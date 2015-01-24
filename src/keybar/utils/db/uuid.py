# Based on the implementation in django-postgres but with various fixes
# and form-integration.
#
# Once Django 1.8 supports this ootb this module can be removed.
import uuid

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from psycopg2.extras import register_uuid

register_uuid()


class UUIDField(models.Field, metaclass=models.SubfieldBase):
    description = "UUID"
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid UUID."),
    }

    def __init__(self, auto=False, *args, **kwargs):
        self.auto = auto
        kwargs['max_length'] = 32

        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True

        super(UUIDField, self).__init__(**kwargs)

    def get_internal_type(self):
        return 'UUIDField'

    def db_type(self, connection):
        return 'uuid'

    def pre_save(self, model_instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """
        value = getattr(model_instance, self.attname, None)

        if self.auto and add and not value:
            # Assign a new value for this attribute if required.
            value = uuid.uuid4()
            setattr(model_instance, self.attname, value)
            value = value.hex
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Casts uuid.UUID values into the format expected by the back end
        """
        if isinstance(value, uuid.UUID):
            value = str(value)
        return value

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, (str, bytes)):
            try:
                return uuid.UUID(value)
            except ValueError:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value}
                )

        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
            'max_length': self.max_length,
        }
        defaults.update(kwargs)
        return super(UUIDField, self).formfield(**defaults)
