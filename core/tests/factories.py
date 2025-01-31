import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    name = factory.Sequence(lambda n: f'{fake.name()}')
    email = factory.Sequence(lambda n: f'{fake.email()}')
    password = factory.Sequence(lambda n: f'{fake.password()}')

class EnterpriseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'companies.Enterprise'

    company_name = factory.Sequence(lambda n: f'{fake.company()}')
    document = factory.Sequence(lambda n: f'{fake.numerify(14 * "#")}')
    user = factory.SubFactory(UserFactory)


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'companies.Employee'

    user = factory.SubFactory(UserFactory)
    enterprise = factory.SubFactory(EnterpriseFactory)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.Group'

    name = factory.Sequence(lambda n: f'{fake.name()}')
    enterprise = factory.SubFactory(EnterpriseFactory)

