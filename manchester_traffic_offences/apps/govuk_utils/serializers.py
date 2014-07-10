import json
from dateutil import parser
from time import mktime

from django.core.serializers.json import DjangoJSONEncoder


def load_with_datetime(pairs):
    d = {}

    for k, v in pairs:
        if isinstance(v, basestring):
            try:
                d[k] = parser.parse(v)
                continue
            except TypeError:
                pass

        d[k] = v
    return d


class DateAwareSerializer(object):
    def dumps(self, obj):
        return json.dumps(obj, cls=DjangoJSONEncoder)

    def loads(self, data):
        return json.loads(data, object_pairs_hook=load_with_datetime)
