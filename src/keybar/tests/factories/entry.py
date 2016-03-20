
import factory

from keybar.models.entry import Entry
from keybar.tests.factories.user import UserFactory


class EntryFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Entry
