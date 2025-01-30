import pytest
from django.contrib.auth.hashers import make_password
from faker import Faker

from accounts.auth import get_token
from accounts.models import User

fake = Faker()


@pytest.fixture
def user():
    """Fixture para criar um usuário para os testes"""
    return User.objects.create(
        name=fake.first_name(),
        email=fake.email(),
        password=make_password('testpassword'),
    )


@pytest.mark.django_db
def test_get_token_with_success(user):
    response = get_token(user)

    assert 'refresh' in response
    assert 'access_token' in response
