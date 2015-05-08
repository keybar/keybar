from django.db import models
from django.utils import timezone

from keybar.utils.db import KeybarModel, sane_repr
from keybar.utils.db.slug import slugify, find_next_increment


class Team(KeybarModel):
    organization = models.ForeignKey('keybar.Organization')

    slug = models.SlugField()
    name = models.CharField(max_length=64)

    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('organization', 'slug'),)

    __repr__ = sane_repr('slug', 'owner_id', 'name')

    def __str__(self):
        return '%s (%s)' % (self.name, self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = find_next_increment(Team, 'slug', slugify(self.name))
        super(Team, self).save(*args, **kwargs)

    @property
    def member_set(self):
        return self.organization.member_set.filter(teams=self, user__is_active=True)


class OrganizationMemberTeam(KeybarModel):
    team = models.ForeignKey(Team)
    organization_member = models.ForeignKey('keybar.OrganizationMember')

    class Meta:
        unique_together = (('team', 'organization_member'),)

    __repr__ = sane_repr('team_id', 'organizationmember_id')
