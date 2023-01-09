# -*- coding: utf-8 -*-
import os

extensions = [
    'sphinx.ext.intersphinx',
    'releases',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'django-uwsgi-admin'
year = '2016-2023'
author = 'django-uwsgi-admin maintainers'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.3.0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'pr': ('https://github.com/ionelmc/django-uwsgi-admin/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
    '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

releases_issue_uri = "https://github.com/unbit/django-uwsgi/issues/%s"
releases_release_uri = "https://github.com/unbit/django-uwsgi/tree/%s"

htmlhelp_basename = project
latex_elements = {}
latex_documents = [('index', f'{project}.tex', f'{project} Documentation', author, 'manual')]
man_pages = [('index', project, f'{project} Documentation', [author], 1)]
texinfo_documents = [('index', project, f'{project} Documentation', author, project, '', 'Miscellaneous')]
intersphinx_mapping = {'uwsgi': ('http://uwsgi-docs.readthedocs.org/en/latest/', None)}
