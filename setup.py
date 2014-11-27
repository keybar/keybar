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
    'py>=1.4.25,<1.5',
    'pytest>=2.6.3,<2.7',
    'pytest-django>=2.7,<2.8',

    # Pep8 and code quality checkers
    'pyflakes>=0.8.1,<0.9',
    'coverage>=3.7.1,<3.8',
    'pytest-cov>=1.8,<1.9',
    'pytest-flakes>=0.2,<1.0',
    'pytest-pep8>=1.0.5,<1.1',
    'pep8>=1.5.7,<1.6',
    'coverage>=3.7.1,<3.8',

    # Fixtures, test helpers
    'factory-boy>=2.4.1,<2.5',
    'mock>=1.0.1,<1.1',
    'httpretty>=0.8.0',
]


install_requires = [
    # General dependencies
    'django>=1.7,<1.8',

    # For async worker support
    'celery>=3.1.15,<3.2',
    'django-celery>=3.1.16,<3.2',

    # i18n/l10n,
    # 'babel>=1.3', -> requirements.txt
    'django-babel-underscore>=0.1.0',
    'django-statici18n>=1.1',
    'django-babel>=0.3.6',

    # For our REST Api
    'djangorestframework>=2.4.3,<2.5',
    'httpsig>=1.1.0,<1.2.0',
    'requests>=2.4.1,<2.5',
    'requests-toolbelt',

    # Markdown support for browsable api
    'markdown',

    # Filtering support for the API
    'django-filter',

    # Form helpers
    'django-floppyforms>=1.2.0',

    # For our development (and probably production?) tls pre-configured
    # server.
    'tornado>=4.0.2,<5.0',

    # All the crypto libs we ever need
    'cryptography>=0.5.4,<1.0',
    'certifi',

    # WSGI utilities
    'werkzeug>=0.9',
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
    },
    zip_safe=False,
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
