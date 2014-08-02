import pytest

from keybar.utils.crypto import xor_strings


def test_xor_strings():
    s = xor_strings(b'Hello World', b'my key')
    assert xor_strings(s, b'my key') == bytearray(b'Hello World')


def test_xor_strings_requires_bytes_as_key():
    with pytest.raises(AssertionError):
        s = xor_strings(b'Hello World', 'my key')


def test_xor_strings_requires_bytes_as_string():
    with pytest.raises(AssertionError):
        s = xor_strings('Hello World', b'my key')
