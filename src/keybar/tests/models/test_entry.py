import pytest
import mock

from keybar.models.entry import Entry


@pytest.mark.django_db
class TestEntry:

    @mock.patch('keybar.models.entry.Fernet')
    def test_simple_encryption_key_derive(self, Fernet):
        expected = b'e5cigLxMyXhKx41ClDT8OqiBDdszhh7oeCA-nOqzWHE='
        Fernet.generate_key.return_value = expected

        entry = Entry(identifier='Something')
        entry.key = Entry.derive_encryption_key_spec(b'password')
        assert entry.get_encryption_key(b'password') == expected
