import pytest


def generate_parameters(source):
    keys = source['keys']
    return pytest.mark.parametrize(keys, [
        tuple([entry[k] for k in keys])
        for entry in source['samples']
    ])


DERIVED_KEY_SAMPLES = {
    'keys': ('salt', 'password', 'expected'),
    'samples': [
        {
            'salt': b'predictable salt',
            'password': '漢語中文',
            'expected': b'J\xcb\x00\x98\xc2\xec\x99\xac\xed\xe6\xe992o\xf5\xe6\xadj"d\xa1W\xbbvo5`\x15b4\x07\x8b',
        },
        {
            'salt': b'predictable salt',
            'password': 'simple string',
            'expected': b'\x13n\xd7\xbf\xceP[W\xfc\x14\xac\x1a/~{\x02\xc1\xa9\x10l\x88\x04\xca\xe5\xfas\xdb^\xd2\x15\xabI',
        },
        {
            'salt': b'predictable salt',
            'password': b'simple bytes string',
            'expected': b"fj\x92\x0fe\x1d\x82\xa2\xfa\x1dp\xcc \x1f}\xdb\xbf\xa13\xf6\xa3'\x80M\xb2\x91\xba6\xe9\xe8\x1b.",
        },
        {
            'salt': b'predictable salt',
            'password': '½³@ſđæ',
            'expected': b'\n\xf3\xa4\x01\x92V\xd7\x88[\xaa\xaa\x90{,1U\xb1N\x98\x01\xdb\x08n\x98u\xc3[L\xe5LV\x9b',
        },
    ]
}
