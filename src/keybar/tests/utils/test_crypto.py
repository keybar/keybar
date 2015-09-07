import os

from django.utils.encoding import force_bytes
from hypothesis import strategies as st
from hypothesis import example, given

from keybar.utils.crypto import (
    derive_encryption_key, fernet_decrypt, fernet_encrypt, get_salt, verify_encryption_key)

from .samples import DERIVED_KEY_SAMPLES, generate_parameters


@generate_parameters(DERIVED_KEY_SAMPLES)
def test_simple_encryption_key_derive_and_verify(salt, password, expected):
    assert derive_encryption_key(salt, password) == expected
    assert verify_encryption_key(salt, password, expected)


@given(salt=st.binary(), password=st.text(), message=st.text())
@example(os.urandom(16), b'my super secure password', '漢語中文')
@example(os.urandom(16), 'my super secure password', '@y1ŋ@¨³¼½¬]@')
@example(os.urandom(16), 'æ¶←@³¬\~]²↓³¼¬ŧ@', 'this is my secure message')
@example(os.urandom(16), '漢語中文', 'this is my secure message')
@example(os.urandom(16), '漢語中文', b'this is my secure message')
def test_encrypt_decrypt_cycle(salt, password, message):
    encrypted = fernet_encrypt(message, salt, password)

    assert isinstance(encrypted, str)

    decrypted = fernet_decrypt(encrypted, salt, password)

    assert isinstance(decrypted, bytes)

    assert decrypted == force_bytes(message)


def test_get_salt():
    assert len(get_salt()) == 32


def test_correct_settings():
    from keybar.conf.base import KEYBAR_KDF_ITERATIONS
    from keybar.conf.development import KEYBAR_KDF_ITERATIONS as DEV_KEYBAR_KDF_ITERATIONS

    assert KEYBAR_KDF_ITERATIONS == 1000000
    assert DEV_KEYBAR_KDF_ITERATIONS == 1000000
