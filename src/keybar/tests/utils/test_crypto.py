import mock
import pytest

from keybar.utils.crypto import (
    xor_strings, derive_encryption_key_spec, get_encryption_key)


def test_xor_strings():
    s = xor_strings(b'Hello World', b'my key')
    assert xor_strings(s, b'my key') == bytearray(b'Hello World')


def test_xor_strings_requires_bytes_as_key():
    with pytest.raises(AssertionError):
        s = xor_strings(b'Hello World', 'my key')


def test_xor_strings_requires_bytes_as_string():
    with pytest.raises(AssertionError):
        s = xor_strings('Hello World', b'my key')


@mock.patch('keybar.utils.crypto.Fernet')
def test_simple_encryption_key_derive(Fernet):
    expected = b'e5cigLxMyXhKx41ClDT8OqiBDdszhh7oeCA-nOqzWHE='
    Fernet.generate_key.return_value = expected

    key = derive_encryption_key_spec(b'password')
    assert get_encryption_key(key, b'password') == expected
