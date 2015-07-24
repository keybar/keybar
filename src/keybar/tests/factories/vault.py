
import factory

from keybar.models.vault import Vault
from keybar.tests.factories.organization import OrganizationFactory
from keybar.utils.test import get_random_name


class VaultFactory(factory.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)

    name = factory.Sequence(lambda i: get_random_name(8, 32))

    class Meta:
        model = Vault
