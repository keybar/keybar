from django.db import models
from django.utils import timezone

from keybar.utils.db import KeybarModel, sane_repr
from keybar.utils.db.slug import find_next_increment, slugify


class TeamVault(KeybarModel):
    vault = models.ForeignKey('keybar.Vault')
    team = models.ForeignKey('keybar.Team')


class Vault(KeybarModel):
    slug = models.SlugField()
    name = models.CharField(max_length=200)

    organization = models.ForeignKey('keybar.Organization')

    teams = models.ManyToManyField(
        'keybar.Team', blank=True,
        through=TeamVault)

    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('organization', 'slug'),)

    __repr__ = sane_repr('organization_id', 'slug')

    def __str__(self):
        return '%s (%s)' % (self.name, self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = find_next_increment(Vault, 'slug', slugify(self.name))
        super(Vault, self).save(*args, **kwargs)
