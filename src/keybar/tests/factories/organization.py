import factory

from keybar.models.organization import Organization, OrganizationMember
from keybar.utils.test import get_random_name

from keybar.tests.factories.user import UserFactory


class OrganizationFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda i: get_random_name(8, 32))
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Organization

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        organization = manager.create(*args, **kwargs)
        OrganizationMemberFactory.create(
            organization=organization,
            user=organization.owner)
        return organization


class OrganizationMemberFactory(factory.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = OrganizationMember
