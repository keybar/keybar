from rest_framework.parsers import JSONParser


class JSONParser(JSONParser):
    """Parses JSON-serialized data.

    This handles our custom media-type properly .
    """
    media_type = 'application/vnd.keybar+json'
