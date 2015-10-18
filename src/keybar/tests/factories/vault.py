
import factory

from keybar.models.vault import Vault
from keybar.tests.factories.user import UserFactory
from keybar.utils.test import get_random_name


class VaultFactory(factory.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)

    name = factory.Sequence(lambda i: get_random_name(8, 32))

    class Meta:
        model = Vault
