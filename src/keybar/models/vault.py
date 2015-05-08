from django.db import models
from django.utils import timezone

from keybar.utils.db import KeybarModel, sane_repr


class TeamVault(KeybarModel):
    vault = models.ForeignKey('keybar.Vault')
    team = models.ForeignKey('keybar.Team')


class Vault(KeybarModel):
    slug = models.SlugField(null=True)
    name = models.CharField(max_length=200)

    organization = models.ForeignKey('keybar.Organization')

    teams = models.ManyToManyField(
        'keybar.Team', blank=True,
        through=TeamVault)

    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('organization', 'slug'),)

    __repr__ = sane_repr('organization_id', 'slug')
