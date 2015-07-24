import os

import pytest
from django.utils.encoding import force_bytes

from keybar.utils.crypto import (
    decrypt, derive_encryption_key, encrypt, get_salt, verify_encryption_key)


@pytest.mark.parametrize('salt,password,expected', (
    (b'predictable salt', '漢語中文',
        b's RU\xb4\x12S\xa7\x83\x1d\xa5\xc23U:`O\x14R\x92\xb30x\xbe{\xac\x1b\xb93\xa5\x8d\xae'),  # noqa
    (b'predictable salt', 'simple string',
        b'Bj=\x81\xb0\x8b\x95\t\xf4\x8f\x8c\x139L\xf9\xc6^8=\x0c\x1d\xa5\xde\xd0\x9f,~\x0b\xde\x05R\xb6'),  # noqa
    (b'predictable salt', b'simple bytes string',
        b'\x7f\xea\xf9\x9b\xa0j\x96jiy\x14~"\xabz \xe5\xe1\xa7IB\xbe<l\xc50)!\xca[Y1'),  # noqa
    (b'predictable salt', '½³@ſđæ',
        b'iS\x14F\xa21\x0bM\xe5\x0fU3X\xcd\xef|&\xa1\xd6\x8f\xac<\xab\xd7\x8d\x12s\xcf\xe8\xea\x00\xf5'),  # noqa
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
