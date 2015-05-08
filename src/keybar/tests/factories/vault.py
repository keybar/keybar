
import factory

from keybar.models.vault import Vault
from keybar.tests.factories.organization import OrganizationFactory


class VaultFactory(factory.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)

    class Meta:
        model = Vault
