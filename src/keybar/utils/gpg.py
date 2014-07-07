import os
import subprocess

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.encoding import force_bytes


if not os.access(GPG_BIN, os.X_OK):
    raise ImproperlyConfigured('Cannot find GnuPG binary at {}'.format(GPG_BIN))


class EncryptionError(Exception):
    """
    This exception is raised to indicate that an error occurred during the
    encryption process. The exception value will be the STDERR output of gpg,
    so this exception should be swallowed by the calling process unless running
    in debug mode.
    """


def encrypt(data, key_ids=None):
    """
    Encrypt data with the public keys as specified as key_ids of the
    application keyring. Data may contain unicode characters, which are sent
    to GPG as UTF-8 data.
    """
    args = [
        settings.GPG_BIN,
        '--encrypt',
        '--no-options',
        '--trust-model',
        'always',
        '--batch',
        '--armor',
    ]

    for key_id in key_ids:
        args += ['--recipient', key_id]

    try:
        gpg = subprocess.Popen(
            args,
            bufsize = 4096,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
        output = gpg.communicate(force_bytes(data))
        if gpg.returncode != 0:
            raise EncryptionError('{0:d}: {0}'.format(gpg.returncode, output[1]))
        return output[0]
    except OSError as exc:
        raise EncryptionError(exc)
