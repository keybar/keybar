# -*- coding: utf-8 -*-
# Some code taken from python-gnupg, Copyright (C) 2008-2014 Vinay Sajip.
import os
import shutil
import tempfile

import mock
import pytest
import gnupg

from django.conf import settings

from keybar.utils import gpg as gpg_util


class TestGPG:

    def setup(self):
        tmp = tempfile.mkdtemp()
        hd = os.path.join(tmp, 'keys')
        if os.path.exists(hd):
            assert os.path.isdir(hd)
            shutil.rmtree(hd)

        self.homedir = hd
        self.gpg = gpg = gnupg.GPG(gnupghome=hd, gpgbinary=settings.GPG_BIN)

        v = gpg.version
        if v:
            if v >= (2,):
                gpg.options = ['--debug-quick-random']
            else:
                gpg.options = ['--quick-random']

    def teardown(self):
        shutil.rmtree(self.homedir)

    def test_environment(self):
        hd = self.homedir
        assert os.path.exists(hd)
        assert os.path.isdir(hd)

    def generate_key(self, first_name, last_name, domain, passphrase=None):
        "Generate a key"
        params = {
            'Key-Type': 'DSA',
            'Key-Length': 1024,
            'Subkey-Type': 'ELG-E',
            'Subkey-Length': 2048,
            'Name-Comment': 'A test user',
            'Expire-Date': 0,
        }
        options = self.gpg.options or []
        if '--debug-quick-random' in options or '--quick-random' in options:
            # If using the fake RNG, a key isn't regarded as valid
            # unless its comment has the text (insecure!) in it.
            params['Name-Comment'] = 'A test user (insecure!)'
        params['Name-Real'] = '%s %s' % (first_name, last_name)
        params['Name-Email'] = ("%s.%s@%s" % (first_name, last_name,
                                              domain)).lower()
        if passphrase is None:
            passphrase = ("%s%s" % (first_name[0], last_name)).lower()
        params['Passphrase'] = passphrase
        cmd = self.gpg.gen_key_input(**params)
        return self.gpg.gen_key(cmd)

    @mock.patch('keybar.utils.gpg.gnupg.GPG')
    def test_encryption_and_decryption(self, GPG):
        GPG.return_value = self.gpg

        key = self.generate_key("Andrew", "Able", "alpha.com", passphrase="andy")
        andrew = key.fingerprint
        key = self.generate_key("Barbara", "Brown", "beta.com", passphrase='bbrown')
        barbara = key.fingerprint

        data = 'Hello, André!'

        encrypted = gpg_util.encrypt(data, [andrew, barbara])

        assert data != encrypted

        decrypted = gpg_util.decrypt(encrypted, passphrase='andy')

        assert decrypted == data
