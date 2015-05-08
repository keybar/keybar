import pytest

from keybar.tests.factories.team import TeamFactory


@pytest.mark.django_db
class TestTeam:

    def test_simple(self):
        team = TeamFactory.create()

        assert str(team) == '{0} ({1})'.format(team.name, team.slug)

    def test_slug(self):
        team = TeamFactory.create(name='This is funny')
        team2 = TeamFactory.create(name='This is funny')

        assert team.slug == 'this-is-funny'
        assert team2.slug == 'this-is-funny-2'
