import re

import unicodedata

from django.conf import settings
from django.utils.encoding import force_text


_slugify_replacement_table = {
    '\xdf': 'ss',
    '\xe4': 'ae',
    '\xe6': 'ae',
    '\xf0': 'dh',
    '\xf6': 'oe',
    '\xfc': 'ue',
    '\xfe': 'th',
}

_slugify_word_re = re.compile(
    r'[^a-zA-Z0-9{0}]+'.format(
        ''.join(re.escape(c) for c in _slugify_replacement_table.keys())
    )
)


def slugify(string, convert_lowercase=True):
    """Slugify a string."""
    string = force_text(string)

    result = []

    if convert_lowercase:
        string = string.lower()

    for word in _slugify_word_re.split(string.strip()):
        if word:
            for search, replace in _slugify_replacement_table.iteritems():
                word = word.replace(search, replace)
            word = unicodedata.normalize('NFKD', word)
            result.append(word.encode('ascii', 'ignore'))

    return '-'.join(result) or '-'


def find_next_increment(model, column, string, **query_opts):
    """Get the next incremented string based on `column` and `string`.

    Example::

        find_next_increment(Organization, 'slug', slugify('organization name'))
    """
    field = model._meta.get_field_by_name(column)[0]
    max_length = field.max_length if hasattr(field, 'max_length') else None

    # We are pretty defensive here and make sure we always have 4 characters
    # left, to be able to append up to 999 slugs (-1 ... -999)
    assert max_length is None or max_length > 4

    slug = string[:max_length - 4] if max_length is not None else string
    filter = {column: slug}
    filter.update(query_opts)

    if not model.objects.filter(**filter).exists():
        return slug

    filter = {'%s__startswith' % column: slug + '-'}
    filter.update(query_opts)

    existing = model.objects.filter(**filter).values_list(column, flat=True)

    # strip of the common prefix
    slug_numbers = [i[len(slug)+1:] for i in existing]

    # find the next free slug number
    slug_numbers = [int(i) for i in slug_numbers if i.isdigit()]
    num = max(slug_numbers) + 1 if slug_numbers else 2

    assert max_length is None or num < 1000

    return '{0}-{1}'.format(slug, num)
