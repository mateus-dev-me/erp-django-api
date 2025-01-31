import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.views import status

from core.tests.factories import UserFactory
from core.tests.factories import EnterpriseFactory

fake = Faker()


@pytest.mark.django_db
class TestUserAPIView:
    def test_create_employee_user_with_success(self, client):
        user = UserFactory.create()
        enterprise = EnterpriseFactory.create(user=user)

        data = {
            'name': fake.name(),
            'email': fake.email(),
            'password': fake.password(),
            'type_account': 'employee',
            'company_id': enterprise.pk,
        }

        url = reverse('signup')
        response = client.generic('POST', url, json=data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'user' in response_data['data']
        assert 'enterprise' in response_data['data']

        user_data = response_data['data']['user']
        assert user_data['name'] == data['name']
        assert user_data['email'] == data['email']

    def test_create_enterprise_user_with_success(self, client):
        data = {
            'name': fake.name(),
            'email': fake.email(),
            'password': fake.password(),
            'company_name': fake.company(),
            'document': fake.numerify(14 * '#'),
        }

        url = reverse('signup')
        response = client.generic('POST', url, json=data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'user' in response_data['data']
        assert 'enterprise' in response_data['data']

        user_data = response_data['data']['user']
        assert user_data['name'] == data['name']
        assert user_data['email'] == data['email']
