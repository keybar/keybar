import factory

from keybar.models.vault import Vault
from keybar.tests.factories.user import UserFactory


class VaultFactory(factory.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)

    name = 'test vault'

    class Meta:
        model = Vault
