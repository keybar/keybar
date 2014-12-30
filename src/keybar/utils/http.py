# -*- coding: utf-8 -*-


class InsecureTransport(Exception):
    pass


def is_secure_transport(uri):
    """Check if the uri is over ssl."""
    return uri.lower().startswith('https://')
