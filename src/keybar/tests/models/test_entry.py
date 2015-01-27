import uuid
import mock

import pytest

from keybar.models.entry import Entry
from keybar.tests.factories.entry import EntryFactory
from keybar.tests.factories.device import DeviceFactory, PRIVATE_KEY


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

    @mock.patch('keybar.models.entry.get_salt')
    def test_set_value_generates_salt(self, mock_get_salt):
        mock_get_salt.return_value = b'salt1'

        entry = EntryFactory.create()

        assert entry.value == b''

        entry.set_value(self.device, 'value', PRIVATE_KEY)
        entry.save()

        assert entry.decrypt(entry.id, self.device.id, PRIVATE_KEY) == b'value'

    def test_set_value_specific_salt(self):
        entry = EntryFactory.create()

        assert entry.value == b''

        entry.set_value(self.device, 'value', 'salt2', PRIVATE_KEY)
        entry.save()

        assert entry.decrypt(entry.id, self.device.id, PRIVATE_KEY) == b'value'

    def test_set_value_does_not_save(self):
        entry = EntryFactory.create()

        assert entry.value == b''

        entry.set_value(self.device, 'value', 'salt2', PRIVATE_KEY)

        assert entry.value

        assert Entry.objects.get(pk=entry.pk).value == b''
