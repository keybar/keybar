import pytest

from keybar.tests.factories.organization import OrganizationFactory


@pytest.mark.django_db
class TestOrganization:

    def test_simple(self):
        org = OrganizationFactory.create()

        assert str(org) == org.name

    def test_slug(self):
        org = OrganizationFactory.create(name='This is funny')
        org2 = OrganizationFactory.create(name='This is funny')

        assert org.slug == 'this-is-funny'
        assert org2.slug == 'this-is-funny-2'
