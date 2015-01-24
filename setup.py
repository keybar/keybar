#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


test_requires = [
    # General test libraries
    'tox>=1.8,<1.9',
    'py>=1.4.26,<1.5',
    'pytest>=2.6.4,<2.7',
    'pytest-django>=2.8,<2.9',

    # Pep8 and code quality checkers
    'pyflakes>=0.8.1,<0.9',
    'coverage>=3.7.1,<3.8',
    'pytest-cov>=1.8.1,<1.9',
    'pytest-flakes>=0.2,<1.0',
    'pytest-pep8>=1.0.5,<1.1',
    'pep8>=1.5.7,<1.6',
    'coverage>=3.7.1,<3.8',

    # Fixtures, test helpers
    'factory-boy>=2.4.1,<2.5',
    'mock>=1.0.1,<1.1',
]


install_requires = [
    # General dependencies
    'django>=1.7.3,<1.8',

    # Configuration
    'django-configurations==0.8',
    'django-cache-url==0.8.0',
    'dj-database-url==0.3.0',
    'djorm-pgarray>=1.2,<1.3',

    # Better user sessions
    'django_user_sessions>=1.1.0,<1.2.0',

    # For async worker support
    'celery>=3.1.17,<3.2',

    # i18n/l10n,
    # 'babel>=1.3', -> requirements.txt
    'django-statici18n>=1.1.1,<1.2',
    'django-babel>=0.3.9',

    # For our REST Api
    'djangorestframework>=3.0.2,<3.1',
    'httpsig>=1.1.0,<1.2.0',
    'requests>=2.5.0,<2.6',
    'requests-toolbelt',

    # Form helpers
    'django-floppyforms>=1.3.0',

    # For our development (and probably production?) tls pre-configured
    # server.
    'tornado>=4.0.2,<5.0',

    # All the crypto libs we ever need
    'cryptography>=0.7.2,<1.0',
    'certifi',
    'qrcode>=5.1,<5.2',
    'pycrypto>=2.6.1,<2.7',

    # Used to generate QR Codes
    'Pillow>=2.7,<2.8',

    # WSGI utilities
    'werkzeug>=0.9',

    # For the client... resides here until we split all the code
    # to a separate repository. Keep it simple for now.
    'httpie>=0.8.0,<1.0',
    'click>=3.3,<3.4',

    # for `generate_identities` script
    'py509',
]


dev_requires = [
    'ipdb'
]


docs_requires = [
    'sphinx>=1.2.3',
    'sphinx_rtd_theme'
]


postgresql_requires = [
    'psycopg2>=2.5.4',
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
