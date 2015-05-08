import uuid

import pytest

from keybar.models.entry import Entry
from keybar.tests.factories.entry import EntryFactory
from keybar.tests.factories.device import DeviceFactory, PRIVATE_KEY
from keybar.tests.factories.user import UserFactory


@pytest.mark.django_db
class TestEntry:

    def setup(self):
        self.device = DeviceFactory.create()

    def test_has_owner(self):
        entry = EntryFactory.create()
        assert entry.owner is not None

    def test_entry_has_uuid_as_primary_key(self):
        entry = EntryFactory.create()

        # raises on invalid uuid
        uuid.UUID(str(entry.pk))

    def test_entry_can_have_tags(self):
        entry = EntryFactory.create()

        # defaults to empty list.
        assert entry.tags is None

        entry.tags = ['tag1', 'tag2']
        entry.save()

        assert Entry.objects.get(pk=entry.pk).tags == ['tag1', 'tag2']

    def test_create_update_decrypt(self):
        user = UserFactory.create()

        entry = Entry.create(self.device.id, 'this is secret', PRIVATE_KEY, owner=user)

        assert entry.salt is not None
        assert entry.decrypt(entry.id, self.device.id, PRIVATE_KEY) == b'this is secret'

        old_salt = entry.salt
        entry.update('this is a new secret', PRIVATE_KEY)
        entry.save()

        # Always generates a new salt.
        assert entry.salt != old_salt

        assert entry.decrypt(entry.id, self.device.id, PRIVATE_KEY) == b'this is a new secret'
