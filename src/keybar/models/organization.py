from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from keybar.utils.db import KeybarModel, sane_repr
from keybar.utils.db.slug import find_next_increment, slugify


class OrganizationManager(models.Manager):
    def get_for_user(self, user):
        """Returns a set of all organizations for a user."""
        return (OrganizationMember.objects
            .filter(user=user)
            .select_related('organization'))


class Organization(KeybarModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    date_added = models.DateTimeField(default=timezone.now)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='keybar.OrganizationMember',
        related_name='organization_memberships'
    )

    objects = OrganizationManager()

    __repr__ = sane_repr('owner_id', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = find_next_increment(Organization, 'slug', slugify(self.name))
        super(Organization, self).save(*args, **kwargs)


class OrganizationMember(KeybarModel):
    OWNER = 'owner'
    ADMIN = 'admin'
    MEMBER = 'member'

    organization = models.ForeignKey(Organization)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='organization_members')

    email = models.EmailField(null=True, blank=True)

    type = models.CharField(max_length=64, choices=(
        (MEMBER, _('Member')),
        (ADMIN, _('Admin')),
        (OWNER, _('Owner')),
    ), default=MEMBER)

    date_added = models.DateTimeField(default=timezone.now)

    teams = models.ManyToManyField(
        'keybar.Team', blank=True,
        through='keybar.OrganizationMemberTeam')

    class Meta:
        unique_together = (
            ('organization', 'user'),
            ('organization', 'email'),
        )

    __repr__ = sane_repr('organization_id', 'user_id', 'type')

    def get_display_name(self):
        return self.user.get_display_name()

    def get_email(self):
        return self.email or self.user.email
