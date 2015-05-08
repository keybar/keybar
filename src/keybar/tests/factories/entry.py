
import factory

from keybar.models.entry import Entry
from keybar.tests.factories.vault import VaultFactory


class EntryFactory(factory.DjangoModelFactory):
    vault = factory.SubFactory(VaultFactory)

    class Meta:
        model = Entry
