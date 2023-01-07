import os
import re
import sys
from collections import defaultdict

from autoapi.mappers.python import PythonData

sys.path.append(os.path.abspath("./../../../rhino_sdk"))
import importlib

import rhino_health

importlib.reload(rhino_health)

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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Rhino SDK'
copyright = '2022, Rhino Health'
author = 'Rhino Health'

# The full version, including alpha/beta/rc tags
release = rhino_health.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "jupyter_sphinx", # TODO: Can't be pip installed on M1 Mac
    "numpydoc",
    "myst_parser",
    "sphinx_sitemap",
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "autoapi.extension",
]

autoapi_type = 'python'
autoapi_dirs = ['./../../../rhino_sdk/rhino_health']
autoapi_options = ['members', 'undoc-members', 'inherited-members', 'show-inheritance', 'show-module-summary', 'special-members']

# CUSTOM SUPPORT FOR INCLUSION/EXCLUSION DEFINITIONS
DECORATOR_INCLUDE = defaultdict(list)
DECORATOR_EXCLUDE = defaultdict(list)
SKIP_CHILDREN_PATHS = set()
OVERRIDE_PATHS = {}

def ignore_system_functions(obj):
    return obj.name.startswith("__")

def check_object_inclusion(obj):
    parent_id = ".".join(obj.id.split('.')[:-1]).strip(".")
    element_name = obj.id.split('.')[-1]
    should_skip = False
    inclusion_definition = DECORATOR_INCLUDE.get(parent_id, None)
    exclusion_definition = DECORATOR_EXCLUDE.get(parent_id, None)
    if inclusion_definition is not None and element_name not in inclusion_definition:
        should_skip = True
    if exclusion_definition is not None and element_name in exclusion_definition:
        should_skip = True
    if parent_id in SKIP_CHILDREN_PATHS:  # Library doesn't auto skip children annoyingly, need a better solution long term
        should_skip = True
    return should_skip

def add_to_definitions(target_definition, parent_obj, defined_path):
    """
    Allows relative or absolute paths
    """
    relative_path = defined_path.replace(parent_obj.id, "").strip(".")
    relative_id = ".".join(relative_path.split('.')[:-1])
    parent_path = ".".join([parent_obj.id, relative_id]).strip(".")
    element_name = relative_path.split('.')[-1]
    target_definition[parent_path].append(element_name)

def check_docstring_override(obj):
    """
    Allow override at the docstring level with @autoapi True or @autoapi False
    """
    cached_override = OVERRIDE_PATHS.get(obj.id, None)
    if cached_override is not None:
        return cached_override
    if "@autoapi True" in obj.docstring:
        obj.docstring = obj.docstring.replace("@autoapi True", "")
        OVERRIDE_PATHS[obj.id] = False
        return False
    elif "@autoapi False" in obj.docstring:
        OVERRIDE_PATHS[obj.id] = True
        return True
    return None

def update_api_inclusion(obj):
    for child in obj.children:
        if isinstance(child, PythonData):
            if child.name == '__api__':
                for defined_path in child.value:
                    add_to_definitions(DECORATOR_INCLUDE, obj, defined_path)
            elif child.name == '__api_exclude__':
                for defined_path in child.value:
                    add_to_definitions(DECORATOR_EXCLUDE, obj, defined_path)

def ignore_inherited(obj):
    """
    By default we will not include inherited functions (note the autoapi_options must include inherited to allow overrides)
    """
    return obj.inherited

def inclusion_support(sphinx_app, object_type, object_name, obj, skip, options):
    """
    This provides support for our decorator to include/exclude specific objects
    To debug this in the IDE, run the script `which sphinx-build` (the result of that eval in shell) with the params
    -M html source build
    from the docs folder
    """
    skip = skip or ignore_system_functions(obj)
    skip = skip or check_object_inclusion(obj)
    skip = skip or ignore_inherited(obj)
    override = check_docstring_override(obj)
    if override is not None:
        skip = override # If we have an override at the docctring level then force that
    if skip:
        SKIP_CHILDREN_PATHS.add(obj.id)  # Library doesn't auto skip children annoyingly, need a better solution long term
    update_api_inclusion(obj)
    return skip

def objname_override(sphinx_app, object_type, object_name, obj, skip, options):
    """
    Allows specifying a custom objname using the @objname <value>
    """
    if "@objname" in obj.docstring:
        m = re.search('@objname[\s]+([\w]+)', obj.docstring)
        objname = m.group(1)
        obj.name = objname
        obj.docstring = re.sub('@objname[\s]+[\w]+', "", obj.docstring)

def setup(sphinx):
    sphinx.connect("autoapi-skip-member", inclusion_support)
    sphinx.connect("autoapi-skip-member", objname_override)

html_baseurl = os.environ.get("SITEMAP_URL_BASE", "http://127.0.0.1:8000/")

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = "_static/rhino_health.png"

# Define the json_url for our version switcher.
# TODO: Need to update github actions to keep old versions of the docs
json_url = "https://rhino_health.github.io/rhino_sdk_docs/_static/switcher.json"

# Define the version we use for matching in the version switcher.
version_match = os.environ.get("DOC_VERSION")
# If the DOC_VERSION does not exist we are not on the hosted page
# If it is an integer, we're in a PR build and the version isn't correct.
if not version_match or version_match.isdigit():
    # For local development, infer the version to match from the package.
    release = rhino_health.__version__
    if "dev" in release:
        version_match = "latest"
        # We want to keep the relative reference if we are in dev mode
        # but we want the whole url if we are effectively in a released version
        json_url = "/_static/switcher.json"
    else:
        version_match = "v" + release

# -- Internationalization ------------------------------------------------
# specifying the natural language populates some key tags
language = "en"

html_theme_options = {
    "external_links": [
        {
            "url": "https://pypi.org/project/rhino_health/",
            "name": "Releases",
        },
        {"url": "https://pandas.pydata.org/pandas-docs/stable/", "name": "Pandas Docs"},
    ],
    # "github_url": "https://github.com/RhinoHealth/rhino_sdk",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/rhino_health/",
            "icon": "fas fa-box",
        },
        {
            "name": "Pandas",
            "url": "https://pandas.pydata.org",
            "icon": "_static/pandas-square.svg",
            "type": "local",
        },
    ],
    "use_edit_page_button": False,
    "show_toc_level": 1,
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
}

# -- Sitemap -------------------------------------------------------------

sitemap_locales = [None]
sitemap_url_scheme = "{link}"

autosummary_generate = True

# -- Extension options -------------------------------------------------------

myst_enable_extensions = [
    # This allows us to use ::: to denote directives, useful for admonitions
    "colon_fence",
]
