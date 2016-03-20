import uuid

import pytest

from keybar.models.entry import Entry
from keybar.tests.factories.device import PRIVATE_KEY, PRIVATE_KEY2, DeviceFactory
from keybar.tests.factories.entry import EntryFactory
from keybar.tests.factories.user import UserFactory


@pytest.mark.django_db
class TestEntry:

    def setup(self):
        self.device = DeviceFactory.create()

    def test_has_user(self):
        entry = EntryFactory.create()
        assert entry.user is not None

    def test_identifier_can_be_blank(self):
        entry = EntryFactory.create()
        assert entry.identifier == ''

    def test_entry_has_uuid_as_primary_key(self):
        entry = EntryFactory.create()

        # raises on invalid uuid
        uuid.UUID(str(entry.pk))

    def test_entry_can_have_tags(self):
        entry = EntryFactory.create()

        # defaults to empty list.
        assert entry.tags == []

        entry.tags = ['tag1', 'tag2']
        entry.save()

        assert Entry.objects.get(pk=entry.pk).tags == ['tag1', 'tag2']

        entry.tags = ['tag1']
        entry.save()

        assert Entry.objects.get(pk=entry.pk).tags == ['tag1']

    def test_values_can_contain_arbitrary_byte_values(self):
        entry = Entry.create(
            self.device.id, {'password': b'secret'},
            user=UserFactory.create())

        assert entry.salt is not None
        assert tuple(entry.values.keys()) == ('password',)

    def test_create_decrypt(self):
        entry = Entry.create(
            self.device.id, {'password': 'secret'},
            user=UserFactory.create())

        assert entry.salt is not None
        assert entry.decrypt('password', self.device, PRIVATE_KEY) == b'secret'

    def test_create_decrypt_wrong_private_key(self):
        entry = Entry.create(
            self.device.id, {'password': 'secret'},
            user=UserFactory.create())

        assert entry.salt is not None
        assert entry.decrypt('password', self.device, PRIVATE_KEY2) is None
