import mock
import base64
import pytest

from keybar.utils.crypto import (
    derive_encryption_key_spec, get_encryption_key,
    encrypt, decrypt)


@mock.patch('keybar.utils.crypto.PBKDF2HMAC.derive')
def test_simple_encryption_key_derive(derive):
    expected = b'e5cigLxMyXhKx41ClDT8OqiBDdszhh7oeCA-nOqzWHE='
    derive.return_value = expected

    key = derive_encryption_key_spec(b'password')
    assert get_encryption_key(key, b'password') == expected


@pytest.mark.parametrize('password,message', (
    (b'my super secure password', '漢語中文'),
    ('my super secure password', '@y1ŋ@¨³¼½¬]@'),
    ('æ¶←@³¬\~]²↓³¼¬ŧ@', 'this is my secure message'),
    ('漢語中文', 'this is my secure message'),
    pytest.mark.xfail(('漢語中文', b'this is my secure message')),
))
def test_encrypt_decrypt_cycle(password, message):

    # This is the value that get's saved in the database.
    encryption_key_spec = derive_encryption_key_spec(password)

    # This is what usually happens when the user encrypts a key.
    encrypted = encrypt(message, get_encryption_key(encryption_key_spec, password))

    decrypted = decrypt(encrypted, get_encryption_key(encryption_key_spec, password))
    assert decrypted == message
