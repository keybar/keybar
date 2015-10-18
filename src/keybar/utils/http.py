# -*- coding: utf-8 -*-
from urllib3.util.url import parse_url


class InsecureTransport(Exception):
    pass


class InvalidHost(Exception):
    pass


def is_secure_transport(uri):
    """Check if the uri is over ssl."""
    return uri.lower().startswith('https://')


def verify_host(url, allowed):
    return parse_url(url).host in allowed
