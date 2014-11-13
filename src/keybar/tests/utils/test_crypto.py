import os
import mock
import base64
import pytest

from keybar.utils.crypto import (
    derive_encryption_key, get_encryption_key,
    encrypt, decrypt)


@pytest.mark.parametrize('salt,password', (
    (os.urandom(16), '漢語中文'),
    (os.urandom(32), 'simple string'),
    (os.urandom(16), b'simple bytes string'),
    (os.urandom(32), '½³@ſđæ'),
))
def test_simple_encryption_key_derive(salt, password):
    key = derive_encryption_key(salt, password)
    assert get_encryption_key(salt, password) == key


@pytest.mark.parametrize('salt,password,message', (
    (os.urandom(16), b'my super secure password', '漢語中文'),
    (os.urandom(16), 'my super secure password', '@y1ŋ@¨³¼½¬]@'),
    (os.urandom(16), 'æ¶←@³¬\~]²↓³¼¬ŧ@', 'this is my secure message'),
    (os.urandom(16), '漢語中文', 'this is my secure message'),
    pytest.mark.xfail((os.urandom(16), '漢語中文', b'this is my secure message')),
))
def test_encrypt_decrypt_cycle(salt, password, message):
    encrypted = encrypt(message, salt, password)

    decrypted = decrypt(encrypted, salt, password)
    assert decrypted == message
