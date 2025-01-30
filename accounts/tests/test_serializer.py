import pytest

from accounts.serializers import UserSerializer

from core.utils.factories import UserFactory


@pytest.mark.django_db
class TestUserSerializer:
    def test_user_serializer_returns_expected_data(self):
        user = UserFactory.create()
        serializer = UserSerializer(user).data

        assert serializer == {
            'id': user.pk,
            'name': user.name,
            'email': user.email,
            'is_owner': bool(user.is_owner),
        }
