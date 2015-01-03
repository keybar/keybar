from __future__ import unicode_literals

import json
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.lookups import BuiltinLookup, Transform
from django.utils import six

import psycopg2.extras

psycopg2.extras.register_json(oid=3802, array_oid=3807)
psycopg2.extras.register_default_json(loads=json.loads)
psycopg2.extras.register_default_jsonb(loads=json.loads)


class JSONField(models.Field):
    description = 'JSON Field'

    def __init__(self, *args, **kwargs):
        self.decode_kwargs = kwargs.pop('decode_kwargs', {
            'parse_float': decimal.Decimal
        })
        self.encode_kwargs = kwargs.pop('encode_kwargs', {
            'cls': DjangoJSONEncoder,
        })
        super(JSONField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'JSONField'

    def db_type(self, connection):
        return 'jsonb'

    def get_db_prep_value(self, value, connection=None, prepared=None):
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if value is None:
            if not self.null and self.blank:
                return ""
            return None
        return json.dumps(value, **self.encode_kwargs)

    def get_prep_lookup(self, lookup_type, value, prepared=False):
        if lookup_type == 'has_key':
            # Need to ensure we have a string, as no other
            # values is appropriate.
            if not isinstance(value, six.string_types):
                value = '%s' % value
        if lookup_type in ['all_keys', 'any_keys']:
            # This lookup type needs a list of strings.
            if isinstance(value, six.string_types):
                value = [value]
            # This will cast numbers to strings, but also grab the keys
            # from a dict.
            value = ['%s' % v for v in value]

        return value

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        if lookup_type in ['contains', 'in']:
            value = self.get_prep_value(value)
            return [value]

        return super(JSONField, self).get_db_prep_lookup(lookup_type, value, connection, prepared)

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        path = 'keybar.utils.db.json.JSONField'
        kwargs.update(
            decode_kwargs=self.decode_kwargs,
            encode_kwargs=self.encode_kwargs
        )
        return name, path, args, kwargs

    def to_python(self, value):
        if value is None and not self.null and self.blank:
            return ''

        if isinstance(value, six.string_types):
            value = json.loads(value)
        return value

    def get_transform(self, name):
        transform = super(JSONField, self).get_transform(name)
        if transform:
            return transform

        if name.startswith('path_'):
            path = '{%s}' % ','.join(name.replace('path_', '').split('_'))
            return PathTransformFactory(path)

        try:
            name = int(name)
        except ValueError:
            pass

        return GetTransform(name)


class PostgresLookup(BuiltinLookup):
    def process_lhs(self, qn, connection, lhs=None):
        lhs = lhs or self.lhs
        return qn.compile(lhs)

    def get_rhs_op(self, connection, rhs):
        return '%s %s' % (self.operator, rhs)


class Has(PostgresLookup):
    lookup_name = 'has'
    operator = '?'

JSONField.register_lookup(Has)


class Contains(PostgresLookup):
    lookup_name = 'contains'
    operator = '@>'

JSONField.register_lookup(Contains)


class In(PostgresLookup):
    lookup_name = 'in'
    operator = '<@'

JSONField.register_lookup(In)


class HasAll(PostgresLookup):
    lookup_name = 'has_all'
    operator = '?&'

JSONField.register_lookup(HasAll)


class HasAny(PostgresLookup):
    lookup_name = 'has_any'
    operator = '?|'

JSONField.register_lookup(HasAny)


class Get(Transform):
    def __init__(self, name, *args, **kwargs):
        super(Get, self).__init__(*args, **kwargs)
        self.name = name

    def as_sql(self, qn, connection):
        lhs, params = qn.compile(self.lhs)
        # So we can run a query of this type against a column that contains
        # both array-based and object-based (and possibly scalar) values,
        # we need to add an additional WHERE clause that ensures we only
        # get json objects/arrays, as per the input type.
        # It would be really nice to be able to see if these clauses
        # have already been applied.
        if isinstance(self.name, six.string_types):
            # Also filter on objects.
            filter_to = "%s @> '{}' AND" % lhs
            self.name = "'%s'" % self.name
        elif isinstance(self.name, int):
            # Also filter on arrays.
            filter_to = "%s @> '[]' AND" % lhs

        return '%s %s -> %s' % (filter_to, lhs, self.name), params


class GetTransform(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        return Get(self.name, *args, **kwargs)


class Path(Transform):
    def __init__(self, path, *args, **kwargs):
        super(Path, self).__init__(*args, **kwargs)
        self.path = path

    def as_sql(self, qn, connection):
        lhs, params = qn.compile(self.lhs)
        # Because path operations only work on non-scalar types, we
        # need to filter out scalar types as part of the query.
        return "({0} @> '[]' OR {0} @> '{{}}') AND {0} #> '{1}'".format(lhs, self.path), params


class PathTransformFactory(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, *args, **kwargs):
        return Path(self.path, *args, **kwargs)
