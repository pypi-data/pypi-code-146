# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import seerai_sphinx_theme
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
import geodesic  # noqa


# -- Project information -----------------------------------------------------

project = 'geodesic-python-api'
copyright = '2021, SeerAI'
author = 'Daniel Wilson and Rob Fletcher'

# The short X.Y version.
version = geodesic.__version__
# The full version, including alpha/beta/rc tags
release = 'main'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxcontrib.katex',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',
    "nbsphinx",
    'sphinxemoji.sphinxemoji',
]

# build the templated autosummary files
autosummary_generate = True
numpydoc_show_class_members = False

# autosectionlabel throws warnings if section names are duplicated.
# The following tells autosectionlabel to not throw a warning for
# duplicated section names that are in different documents.
autosectionlabel_prefix_document = True


mathjax_path = "https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# katex options
#
#

katex_prerender = True

napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

coverage_ignore_modules = []

coverage_ignore_functions = []

coverage_ignore_classes = []

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Disable docstring inheritance
autodoc_inherit_docstrings = False

# Disable displaying type annotations, these can be very verbose
autodoc_typehints = 'none'

# Set the order that members should be documented
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'seerai_sphinx_theme'
html_theme_path = [seerai_sphinx_theme.get_html_theme_path()]

html_theme_options = {
    'pytorch_project': 'docs',
    'canonical_url': 'https://seerai.space',
    'collapse_navigation': False,
    'display_version': True,
    'logo_only': True,
}

html_logo = '_static/img/Logo.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', '_templates/_static']

html_context = {
    'css_files': [
        # 'https://fonts.googleapis.com/css?family=Lato',
        # '_static/css/pytorch_theme.css'
        '_static/css/theme.css'
    ],
}

intersphinx_mapping = {'https://docs.python.org/': None}
