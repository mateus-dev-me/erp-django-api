from json import dumps as json_dumps
from typing import Any, Dict, Optional, Union

import pytest
from django.test.client import Client as DjangoClient
from django.utils.http import urlencode

from accounts.models import User
from core.tests.factories import EnterpriseFactory, UserFactory


class Client(DjangoClient):
    """
    Subclasse do DjangoClient que adiciona suporte a parâmetros de consulta (`query_params`)
    e a dados no formato JSON.

    Métodos:
        generic: Faz uma requisição HTTP genérica com suporte adicional para JSON e parâmetros de consulta.
    """

    def generic(
        self,
        method: str,
        path: str,
        data: Union[str, bytes] = '',
        content_type: str = 'application/json',
        secure: bool = False,
        *,
        query_params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **extra: Any,
    ):
        if query_params:
            path = f'{path}?{urlencode(query_params, True)}'

        if json:
            return super().generic(
                method,
                path,
                data=json_dumps(json),
                content_type='application/json',
                secure=secure,
                **extra,
            )
        return super().generic(
            method,
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            **extra,
        )


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user_enterprise():
    user_data = UserFactory.build()
    user = User.objects.create(
        email=user_data.email,
        password=user_data.password,
    )
    EnterpriseFactory.create(user=user)
    return user_data


@pytest.fixture
def user_employee():
    user_data = UserFactory.build()
    user = User.objects.create(
        email=user_data.email,
        password=user_data.password,
    )
    EnterpriseFactory.create(user=user)
    return user_data
