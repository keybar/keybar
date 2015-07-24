import factory

from keybar.models.organization import OrganizationMember
from keybar.models.team import OrganizationMemberTeam, Team
from keybar.tests.factories.organization import OrganizationFactory, OrganizationMemberFactory
from keybar.utils.test import get_random_name


class TeamFactory(factory.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)

    name = factory.Sequence(lambda i: get_random_name(8, 32))

    class Meta:
        model = Team

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        team = manager.create(*args, **kwargs)
        org_member = OrganizationMember.objects.get(user=team.organization.owner)

        OrganizationMemberTeamFactory.create(
            organization_member=org_member,
            team=team)

        return team


class OrganizationMemberTeamFactory(factory.DjangoModelFactory):
    organization_member = factory.SubFactory(OrganizationMemberFactory)
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = OrganizationMemberTeam
