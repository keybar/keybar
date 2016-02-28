from django.db import models
from django.utils import timezone

from keybar.utils.db import KeybarModel, sane_repr
from keybar.utils.db.slug import find_next_increment, slugify


class Vault(KeybarModel):
    slug = models.SlugField()
    name = models.CharField(max_length=200)

    owner = models.ForeignKey('keybar.User')

    date_added = models.DateTimeField(default=timezone.now)

    __repr__ = sane_repr('owner_id', 'slug')

    def __str__(self):
        return '{} ({})'.format(self.name, self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = find_next_increment(Vault, 'slug', slugify(self.name))
        super(Vault, self).save(*args, **kwargs)
