from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import UserManager as BaseUserManager


class ExtendedQuerySet(QuerySet):

    def update_or_create(self, *args, **kwargs):
        obj, created = self.get_or_create(*args, **kwargs)

        if not created:
            fields = dict(kwargs.pop("defaults", {}))
            fields.update(kwargs)
            for key, value in fields.items():
                setattr(obj, key, value)
            obj.save()

        return obj


class ExtendedManager(models.Manager):

    """Manager supporting :meth:`update_or_create`."""

    def get_query_set(self):
        return ExtendedQuerySet(self.model)

    def update_or_create(self, *args, **kwargs):
        return self.get_query_set().update_or_create(**kwargs)


class UserManager(BaseUserManager, ExtendedManager):
    pass
