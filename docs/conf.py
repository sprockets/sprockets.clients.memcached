#!/usr/bin/env python
import sphinx_rtd_theme

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.inheritance_diagram',
    'sphinxcontrib.httpdomain',
]
templates_path = []
source_suffix = '.rst'
master_doc = 'index'
project = 'sprockets.clients.memcached'
copyright = '2014-2018, AWeber Communications'
version = '1.1.0'
release = '1.1'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
intersphinx_mapping = {'python': ('https://docs.python.org/2/', None)}
