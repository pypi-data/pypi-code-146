"""Sphinx configuration for Budo Systems."""
#
#  Copyright (c) 2020-2022.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

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
# from typing import Any

import os
import sys

# sys.path.insert(0, os.path.abspath('.'))
# sys.path.insert(1, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../src'))
# print(f"{sys.path=}")

def list_files(startpath: str) -> None:
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


# list_files(sys.path[0])

# import setup

# -- Project information -----------------------------------------------------

project = 'Budo Systems'
# noinspection PyShadowingBuiltins
copyright = '2020-2022, Joël Larose'
author = 'Joël Larose'

# The full version, including alpha/beta/rc tags
# release = setup.version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx_git',
    # 'sphinxcontrib.apidoc',
    'sphinxcontrib.plantuml',
]

# Add any paths that contain templates here, relative to this directory.
templates_path: list[str] = [
        '_templates',
        # '_templates/autosummary',
        # '_templates/apidoc',
    ]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []

primary_domain = 'py'

default_role = 'py:obj'

add_module_names = False

modindex_common_prefix = [
        'budosystems.',
        'budosystems.adapters.',
        'budosystems.dsl.',
        'budosystems.events.',
        'budosystems.models.',
        'budosystems.services.',
        'budosystems.storage.',
        'budosystems.xtra.',
]

autosectionlabel_prefix_document = True

intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'attrs': ('https://www.attrs.org/en/stable/', None),
}

autosummary_generate = ['api']
autosummary_generate_overwrite = True

autoclass_content = 'class'
autodoc_class_signature = 'separated'

autodata = {
        'no-value': True,
}

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': False,
    'private-members': False,
    'undoc-members': True,
    'inherited-members': False,
    'show-inheritance': True,
    'exclude-members': '__weakref__'
}

events_message_bus = 'budosystems.events.message_bus'
models_contact = 'budosystems.models.contact'
models_typehints = 'budosystems.typehints'
storage_query = 'budosystems.storage.query'
autodoc_type_aliases = {
        # defined in events.message_bus
        'AsyncEventHandler': events_message_bus + '.AsyncEventHandler',
        'Registration': events_message_bus + '.Registration',

        # defined in models.contact
        'OptStrEllipsis': models_contact + '.OptStrEllipsis',

        # defined in models.typehints
        'IMapStrAny': models_typehints + '.IMapStrAny',
        'MMapStrAny': models_typehints + '.MMapStrAny',
        'DictStrAny': models_typehints + '.DictStrAny',
        'DictStrBool': models_typehints + '.DictStrBool',
        'OptStr': models_typehints + '.OptStr',
        'OptInt': models_typehints + '.OptInt',
        'OptBool': models_typehints + '.OptBool',
        'OptDate': models_typehints + '.OptDate',
        'OptDateTime': models_typehints + '.OptDateTime',
        'OptTime': models_typehints + '.OptTime',
        'OptTimeDelta': models_typehints + '.OptTimeDelta',
        'Bases': models_typehints + '.Bases',
        'BoolBinOp': models_typehints + '.BoolBinOp',
        'StrProperty': models_typehints + '.StrProperty',
        'IntProperty': models_typehints + '.IntProperty',

        # defined in storage.query
        'Predicate': storage_query + '.Predicate',
}


todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'haiku'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_style = 'budosystems.css'

# -- PlantUML Options --------------------------------------------------------
plantuml_jar = os.path.join(os.path.abspath('..'), 'plantuml.1.2021.4.jar')
plantuml = f"java -jar {plantuml_jar}"
plantuml_output_format = 'svg_img'
