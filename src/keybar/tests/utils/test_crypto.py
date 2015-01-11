import os
import pytest
from django.utils.encoding import force_bytes

from keybar.utils.crypto import (
    derive_encryption_key, verify_encryption_key,
    encrypt, decrypt, get_salt)


@pytest.mark.parametrize('salt,password,expected', (
    (b'predictable salt', '漢語中文',
        b'\xd3\x85\x8c\x08\xf5\x11\x99\xf5\xca\xad\x1c\x89\xb6<_\x00\xd4u>\xba\x94\niE\xf4\xbeY\xf5\x87\x1d\xf3\x18'),  # noqa
    (b'predictable salt', 'simple string',
        b'#\x1ak\x12\xcf18[\x81\x85\x92\xb1\x80\x93\x0c\x10\xdc\x00\xee\x86\xae6,"{n\x832\xf9r\xca\xbd'),  # noqa
    (b'predictable salt', b'simple bytes string',
        b"9:\xad\x84f+\xbf\xfb'\x81\xb1\xffe>,=\xdb\xc1\xe3\xf6H\xc2\x88\xeb\x1a>\xd8|~qQ#"),  # noqa
    (b'predictable salt', '½³@ſđæ',
        b'F\x1c\xa8;j\xffWl\x10\r\x97x\xaf\xb7\x95\xd2`\x9a\x11z4\xf6\xc3N\x92D\xde\x05?^BN'),  # noqa
))
def test_simple_encryption_key_derive_and_verify(salt, password, expected):
    assert derive_encryption_key(salt, password) == expected
    assert verify_encryption_key(salt, password, expected)


@pytest.mark.parametrize('salt,password,message', (
    (os.urandom(16), b'my super secure password', '漢語中文'),
    (os.urandom(16), 'my super secure password', '@y1ŋ@¨³¼½¬]@'),
    (os.urandom(16), 'æ¶←@³¬\~]²↓³¼¬ŧ@', 'this is my secure message'),
    (os.urandom(16), '漢語中文', 'this is my secure message'),
    pytest.mark.xfail((os.urandom(16), '漢語中文', b'this is my secure message')),
))
def test_encrypt_decrypt_cycle(salt, password, message):
    encrypted = encrypt(message, salt, password)

    assert isinstance(encrypted, bytes)

    decrypted = decrypt(encrypted, salt, password)

    assert isinstance(decrypted, bytes)

    assert decrypted == force_bytes(message)


def test_get_salt():
    assert len(get_salt()) == 32
