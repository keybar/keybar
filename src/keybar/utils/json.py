from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
import json

import datetime
import uuid


class BetterJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        elif isinstance(obj, (set, frozenset)):
            return list(obj)
        return super(BetterJSONEncoder, self).default(obj)


def better_decoder(data):
    return data


def dumps(value, **kwargs):
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
    return force_text(json.dumps(value, cls=BetterJSONEncoder, **kwargs))


def loads(value, **kwargs):
    return json.loads(force_text(value), object_hook=better_decoder)
