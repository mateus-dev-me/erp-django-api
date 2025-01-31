import pytest

from accounts.models import User

from core.tests.factories import UserFactory


@pytest.mark.django_db
class TestUser:
    def test_user_creation_persists_in_database(self):
        UserFactory.create()

        assert User.objects.count() == 1
