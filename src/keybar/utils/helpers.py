from django.contrib.sessions.serializers import JSONSerializer as BaseJSONSerializer

from keybar.utils import json


class UUIDCapableJSONSerializer(BaseJSONSerializer):
    def dumps(self, obj):
        return json.dumps(obj).encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))
