import uuid
import json

from django.core.serializers.json import DjangoJSONEncoder as BaseDjangoJSONEncoder
from django.contrib.sessions.serializers import JSONSerializer as BaseJSONSerializer


class DjangoJSONEncoder(BaseDjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return super(DjangoJSONEncoder, self).default(obj)


class UUIDCapableJSONSerializer(BaseJSONSerializer):
    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':'), cls=DjangoJSONEncoder).encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))
