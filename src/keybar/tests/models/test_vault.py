import pytest

from keybar.tests.factories.vault import VaultFactory


@pytest.mark.django_db
class TestVault:

    def test_simple(self):
        vault = VaultFactory.create()

        assert str(vault) == '{} ({})'.format(vault.name, vault.slug)

    def test_slug(self):
        vault = VaultFactory.create(name='This is funny')
        vault2 = VaultFactory.create(name='This is funny')

        assert vault.slug == 'this-is-funny'
        assert vault2.slug == 'this-is-funny-2'
