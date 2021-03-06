# -*- coding: utf-8 -*-
import os

import django
import pkg_resources


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.conf.development')

django.setup()

try:
    import sphinx_rtd_theme
except ImportError:
    sphinx_rtd_theme = None


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'keybar'
copyright = u'2014, keybar'

dist = pkg_resources.get_distribution('keybar')
version = release = dist.version

exclude_patterns = []

pygments_style = 'sphinx'

if sphinx_rtd_theme:
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = 'default'

html_static_path = ['_static']

htmlhelp_basename = 'keybardoc'

latex_elements = {}

latex_documents = [
    ('index', 'keybar.tex', u'keybar Documentation',
     u'keybar', 'manual'),
]

man_pages = [
    ('index', 'keybar', u'keybar Documentation',
     [u'keybar'], 1)
]

texinfo_documents = [
    ('index', 'keybar', u'keybar Documentation',
     u'keybar', 'keybar', 'Secure password storage',
     'Miscellaneous'),
]

epub_title = u'Keybar - secure password storage'
epub_author = u'Christopher Grebs'
epub_publisher = u'Christopher Grebs'
epub_copyright = u'2014, Christopher Grebs'

intersphinx_mapping = {'http://docs.python.org/': None}
