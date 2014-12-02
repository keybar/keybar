
import factory

from keybar.models.entry import Entry
from keybar.tests.factories.user import UserFactory


class EntryFactory(factory.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Entry
