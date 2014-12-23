# -*- coding: utf-8 -*-
from hashlib import md5
from urllib.parse import urlencode

from django.conf import settings
from allauth.socialaccount.models import SocialAccount


SECURE_BASE_URL = 'https://secure.gravatar.com/avatar/'
PROFILE_URL = 'http://www.gravatar.com/'
FACEBOOK_URL = 'http://graph.facebook.com/{}/picture?width=40&height=40'
RATINGS = ('g', 'pg', 'r', 'x')
MAX_SIZE = 512
MIN_SIZE = 1
DEFAULTS = ('404', 'mm', 'identicon', 'monsterid', 'wavatar', 'retro')


def email_hash(string):
    return md5(str(string.strip().lower()).encode('utf-8')).hexdigest()


def get_gravatar(email, rating='g', size=80, default='mm'):
    """Generate a link to the users' Gravatar."""
    assert rating.lower() in RATINGS
    assert MIN_SIZE <= size <= MAX_SIZE

    url = SECURE_BASE_URL

    options = (('s', size), ('r', rating), ('d', default))
    url += email_hash(email) + '?' + urlencode(options)
    return url


def get_profile_image(user):
    qset = user.socialaccount_set.all()

    if qset.filter(provider='facebook').exists():
        facebook = qset.filter(provider='facebook').first()
        return FACEBOOK_URL.format(facebook.uid)

    return get_gravatar(user.email)
