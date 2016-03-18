#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import find_packages, setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


test_requires = [
    # General test libraries
    'tox==2.3.1',
    'pytest==2.9.0',
    'pytest-django==2.9.1',
    'pytest-isort==0.1.0',

    # Pep8 and code quality checkers
    'flake8==2.5.4',
    'pytest-cov==2.2.1',
    'coverage==4.0.3',

    # Fixtures, test helpers
    'factory-boy==2.6.1',
    'mock==1.3.0',
    'hypothesis==3.1.0',
    'hypothesis-pytest==0.19.0',
]


install_requires = [
    # General dependencies
    'django==1.9.4',

    # For async worker support
    'celery==3.1.23',

    # i18n/l10n,
    'babel==2.2.0',
    'django-babel==0.5.0',

    # For our REST Api
    'djangorestframework==3.3.3',
    'requests==2.9.1',
    'urllib3==1.14',
    'requests-toolbelt==0.6.0',

    # For our development (and probably production?) tls pre-configured server.
    'tornado==4.3',

    # All the crypto libs we ever need
    'cryptography==1.3',
    'certifi==2016.2.28',
    'qrcode==5.2.2',

    # Used to generate QR Codes
    'Pillow==3.1.1',

    # WSGI utilities
    'werkzeug==0.11.4',

    # For the client... resides here until we split all the code
    # to a separate repository. Keep it simple for now.
    'click==6.3',

    # for `generate_identities` script
    'py509==0.1.0',

    # For proper timezone support.
    'pytz==2016.1',
]


docs_requires = [
    'sphinx==1.3.6',
    'sphinx_rtd_theme'
]


postgresql_requires = [
    'psycopg2==2.6.1',
]


redis_requires = [
    'redis==2.10.5',
]

setup(
    name='keybar',
    version='0.1.0',
    description='secure your life!',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='https://github.com/keybar/keybar/',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    test_suite='src',
    tests_require=test_requires,
    install_requires=install_requires,
    extras_require={
        'docs': docs_requires,
        'tests': test_requires,
        'postgresql': postgresql_requires,
        'redis': redis_requires,
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'keybar-server=keybar.server:run_server'
        ]
    },
    license='BSD',
    classifiers=[
        '__DO NOT UPLOAD__',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
