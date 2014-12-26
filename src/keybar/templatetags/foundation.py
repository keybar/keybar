from django import template
from django.utils.safestring import mark_safe
from django.contrib.messages import constants as message_constants


register = template.Library()


ERROR_LEVEL_MAPPING = {
    message_constants.DEBUG: 'secondary',
    message_constants.INFO: '',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'alert'
}

PROVIDER_REPLACEMENTS = {
    'google': 'google_plus',
}


@register.simple_tag
def map_error_level(level):
    return mark_safe(ERROR_LEVEL_MAPPING[level])


@register.simple_tag
def provider_icon(provider):
    if provider.id not in PROVIDER_REPLACEMENTS:
        return provider.id
    return PROVIDER_REPLACEMENTS[provider.id]
