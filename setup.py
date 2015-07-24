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
    'tox>=1.9.2,<2.0.0',
    'pytest>=2.7.0,<2.8',
    'pytest-django>=2.8,<2.9',
    'pytest-isort==0.1.0',

    # Pep8 and code quality checkers
    'pyflakes>=0.8.1,<0.9',
    'coverage>=3.7.1,<3.8',
    'pytest-cov>=1.8.1,<1.9',
    'pytest-flakes>=0.2,<1.0',
    'pytest-pep8>=1.0.5,<1.1',
    'pep8>=1.6.2,<1.7',
    'coverage>=3.7.1,<3.8',

    # Fixtures, test helpers
    'factory-boy>=2.5.1,<2.6',
    'mock>=1.0.1,<1.1',
]


install_requires = [
    # General dependencies
    'django>=1.8.3,<1.9',

    # Configuration
    'django-configurations==0.8',
    'django-cache-url==0.8.0',
    'dj-database-url==0.3.0',

    # User login, sessions, social integration
    'django_user_sessions>=1.1.1,<1.2.0',
    'django-allauth>=0.22.0,<0.23',

    # For async worker support
    'celery>=3.1.17,<3.2',

    # i18n/l10n,
    # 'babel>=1.3', -> requirements.txt
    'django-statici18n>=1.1.2,<1.2',
    'django-babel>=0.3.9',

    # For our REST Api
    'djangorestframework>=3.1.3,<3.2',
    'httpsig>=1.1.2,<1.2.0',
    'requests>=2.6.0,<2.7',
    'requests-toolbelt>=0.4,<0.5',

    # Form helpers
    'django-floppyforms>=1.3.0',

    # For our development (and probably production?) tls pre-configured server.
    'tornado>=4.1,<5.0',

    # All the crypto libs we ever need
    'cryptography>=0.8.1,<1.0',
    'certifi',
    'qrcode>=5.1,<5.2',
    'pycrypto>=2.6.1,<2.7',

    # Used to generate QR Codes
    'Pillow>=2.8,<2.9',

    # WSGI utilities
    'werkzeug>=0.9',

    # For the client... resides here until we split all the code
    # to a separate repository. Keep it simple for now.
    'httpie>=0.9.2,<1.0',
    'click>=4.0,<5.0',

    # for `generate_identities` script
    'py509>=0.0.5',

    # For proper timezone support.
    'pytz>=2015.2',
]


dev_requires = [
    'ipdb'
]


docs_requires = [
    'sphinx>=1.2.3',
    'sphinx_rtd_theme'
]


postgresql_requires = [
    'psycopg2>=2.6',
]


redis_requires = [
    'redis>=2.8.0',
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
        'dev': dev_requires,
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
    ],
)
