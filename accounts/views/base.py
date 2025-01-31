from typing import Dict, List

from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from accounts.exceptions import (
    EnterpriseAlreadyExistsException,
    EnterpriseNotFoundException,
    InvalidAccountTypeException,
    UserAlreadyExistsException,
    UserNotFoundError,
)
from accounts.models import GroupPermissions, User, UserGroups
from companies.models import Employee, Enterprise
from core.exceptions import MissingFieldException


class Base(APIView):
    """Base class providing utility methods for user and enterprise
    management."""

    @classmethod
    def validate_not_null(self, **kwargs) -> None:
        """Validate that the provided fields are not null or empty."""
        for field, value in kwargs.items():
            if not value:
                raise MissingFieldException(
                    f"O campo '{field}' não pode ser vazio."
                )

    @classmethod
    def _validate_type_account(self, type_account: str) -> None:
        """Validate the account type."""
        if type_account not in {'owner', 'employee'}:
            raise InvalidAccountTypeException()

    @classmethod
    def verify_user_exists(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        return User.objects.filter(email=email).exists()

    @classmethod
    def verify_enterprise_exists(self, document: str) -> bool:
        """Check if an enterprise with the given CNPJ exists."""
        return Enterprise.objects.filter(document=document).exists()

    @classmethod
    def get_user(self, email: str, password: str) -> User:
        """
        Retrieve a user by email and check password.

        Raises:
            AuthenticationFailed: If the user does not exist or the password
            is invalid.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Email e/ou senha incorreto(s)')

        if not user.password or not check_password(password, user.password):
            raise AuthenticationFailed('Email e/ou senha incorreto(s)')

        return user

    def get_enterprise_user(self, user_id: int) -> Dict:
        """
        Retrieve enterprise user information including permissions.

        Args:
            user_id: The ID of the user.

        Returns:
            A dictionary with user permissions or an empty list if none exist.
        """
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise UserNotFoundError()

        if not user.is_owner:
            employee = (
                Employee.objects.filter(user_id=user.id)
                .select_related('enterprise')
                .first()
            )
            enterprise = employee.enterprise

            return {
                'id': enterprise.id,
                'name': enterprise.company_name,
                'document': enterprise.document,
                'permissions': self._get_user_permissions(user_id),
            }

        enterprise = Enterprise.objects.filter(user_id=user.id).first()
        return {
            'id': enterprise.id,
            'name': enterprise.company_name,
            'document': enterprise.document,
            'permissions': [],
        }

    @classmethod
    def _get_user_permissions(self, user_id: int) -> List[Dict[str, str]]:
        """Retrieve the permissions for a given user."""
        permissions = (
            GroupPermissions.objects.filter(
                group_id__in=UserGroups.objects.filter(
                    user_id=user_id
                ).values_list('group_id', flat=True)
            )
            .select_related('permission')
            .distinct()
        )

        return [
            {
                'id': p.permission.id,
                'label': p.permission.name,
                'codename': p.permission.codename,
            }
            for p in permissions
        ]

    # pylint: disable=too-many-arguments
    # @transaction.atomic
    # def create_user(
    #     self,
    #     name: str,
    #     email: str,
    #     password: str,
    #     type_account: str = 'owner',
    #     company_id: Optional[int] = None,
    #     company_name: Optional[str] = None,
    #     document: Optional[str] = None,
    # ) -> User:  # noqa: PLR0913, PLR0917

    @transaction.atomic
    def create_user(self, **kwargs) -> User:  # noqa: PLR0913, PLR0917
        self.validate_not_null(
            name=kwargs.get('name'),
            email=kwargs.get('email'),
            password=kwargs.get('password'),
        )

        if self.verify_user_exists(email=kwargs.get('email')):
            raise UserAlreadyExistsException()

        self._validate_type_account(kwargs.get('type_account'))

        if (
            kwargs.get('type_account') == 'employee'
            and not Enterprise.objects.filter(
                id=kwargs.get('company_id')
            ).exists()
        ):
            raise EnterpriseNotFoundException()

        user = User.objects.create(
            name=kwargs.get('name'),
            email=kwargs.get('email'),
            password=make_password(kwargs.get('password')),
        )

        if kwargs.get('type_account') == 'owner':
            self._create_enterprise_user(
                kwargs.get('company_name'),
                kwargs.get('document'),
                user.pk,
            )
        elif kwargs.get('type_account') == 'employee':
            user.is_owner = False
            user.save()
            self._create_employee_user(kwargs.get('company_id'), user.pk)

        return user

    @classmethod
    def _create_enterprise_user(
        self, company_name: str, document: str, user_id: int
    ) -> None:
        """Create an enterprise and associate it with a user."""
        self.validate_not_null(company_name=company_name, document=document)

        if self.verify_enterprise_exists(document=document):
            raise EnterpriseAlreadyExistsException()

        Enterprise.objects.create(
            company_name=company_name,
            document=document,
            user_id=user_id,
        )

    @classmethod
    def _create_employee_user(self, company_id: int, user_id: int) -> None:
        """Create an employee and associate it with an enterprise."""
        if not company_id:
            raise MissingFieldException('O company_id não pode ser vazio.')

        Employee.objects.create(
            enterprise_id=company_id,
            user_id=user_id,
        )
