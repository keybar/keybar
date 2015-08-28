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
            'expected': b's RU\xb4\x12S\xa7\x83\x1d\xa5\xc23U:`O\x14R\x92\xb30x\xbe{\xac\x1b\xb93\xa5\x8d\xae',
        },
        {
            'salt': b'predictable salt',
            'password': 'simple string',
            'expected': b'Bj=\x81\xb0\x8b\x95\t\xf4\x8f\x8c\x139L\xf9\xc6^8=\x0c\x1d\xa5\xde\xd0\x9f,~\x0b\xde\x05R\xb6',
        },
        {
            'salt': b'predictable salt',
            'password': b'simple bytes string',
            'expected': b'\x7f\xea\xf9\x9b\xa0j\x96jiy\x14~"\xabz \xe5\xe1\xa7IB\xbe<l\xc50)!\xca[Y1',
        },
        {
            'salt': b'predictable salt',
            'password': '½³@ſđæ',
            'expected': b'iS\x14F\xa21\x0bM\xe5\x0fU3X\xcd\xef|&\xa1\xd6\x8f\xac<\xab\xd7\x8d\x12s\xcf\xe8\xea\x00\xf5',
        },
    ]
}
