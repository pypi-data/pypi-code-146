#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import snakecdysis
from snakecdysis.global_variable import *

def capitalize_maj(s):
    return s[0].upper() + s[1:]


# -- Path setup --------------------------------------------------------------
PKGNAME = capitalize_maj("snakecdysis")

# The short X.Y version.
version = snakecdysis.__version__
# The full version, including alpha/beta/rc tags
release = snakecdysis.__version__

# -- Project information -----------------------------------------------------
# General information about the project.

project = PKGNAME
copyright = '2022, S Ravel (CIRAD)'
github_doc_root = f'{GIT_URL}/tree/master/docs/'
issues_github_path = f'{GIT_URL}/issues'

latex_authors = '''Sebastien Ravel (CIRAD)'''

## -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.intersphinx',
              'sphinx.ext.viewcode',
              # 'sphinx.ext.autodoc',
              #'sphinx.ext.autosectionlabel',
              # 'autodocsumm',
              'sphinx_copybutton',
              'sphinx_rtd_theme',
              'sphinx_automodapi.automodapi',
              'sphinx.ext.napoleon',
              #'sphinxcontrib.autoprogram'
              ]

# autosectionlabel_prefix_document = True
# autosectionlabel_maxdepth = 4
# autosummary_generate = True
# autosummary_generate_overwrite = False
# numpydoc settings
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False
numpydoc_attributes_as_param_list = False
numpydoc_class_members_toctree = False

# Napoleon settings
napoleon_google_docstring = True
# napoleon_numpy_docstring = False
# napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = ['.rst', "md"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'

master_doc = 'index'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
html_css_files = ["theme.css"]
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
        'canonical_url'             : '',
        'analytics_id'              : 'UA-XXXXXXXXXXXXX-1',  # Provided by Google in your dashboard
        'logo_only'                 : False,
        'display_version'           : True,
        'prev_next_buttons_location': 'bottom',
        'style_external_links'      : False,
        # Toc options
        'collapse_navigation'       : False,
        'sticky_navigation'         : True,
        'navigation_depth'          : 2,
        'includehidden'             : False,
        'titles_only'               : False
}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = PKGNAME

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = PKGNAME

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = f'_images/{PKGNAME}_logo.png'
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = f'_images/{PKGNAME}_logo_short.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# -- Options for LaTeX output ---------------------------------------------
latex_engine = 'pdflatex'

latex_elements = {
        # The paper size ('letterpaper' or 'a4paper').
        'papersize'        : 'a4paper',
        # The font size ('10pt', '11pt' or '12pt').
        'pointsize'        : '12pt',
        # Latex figure (float) alignment
        'figure_align'     : 'htbp',
        'extraclassoptions': 'openany',
        'preamble'         : r'''
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%add number to subsubsection 2=subsection, 3=subsubsection
        \setcounter{secnumdepth}{0}
        %%%% Table of content upto 2=subsection, 3=subsubsection
        \setcounter{tocdepth}{2}
    ''',

        'sphinxsetup'      : \
            'hmargin={0.7in,0.7in}, vmargin={0.7in,0.7in}, \
        marginpar=1in, \
        verbatimwithframe=False, \
        TitleColor={rgb}{0,0,0}, \
        HeaderFamily=\\rmfamily\\bfseries, \
        InnerLinkColor={rgb}{0,0,1}, \
        OuterLinkColor={rgb}{0,0,1}',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).

latex_documents = [
        ('index', f'{PKGNAME}.tex', 'Documentation',
         latex_authors, 'manual', True),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = f'_images/{PKGNAME}_logo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True

latex_toplevel_sectioning = 'section'

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [

]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [

]


# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# def setup(app):
#     app.add_css_file('logo.css')  # may also be an URL('logo.css')  # may also be an URL
    # app.add_css_file('sphinx-argparse.css')

    # from sphinx.ext import apidoc
    # app.connect('builder-inited', lambda _: apidoc.main([
    #         '-o', './docs/source/scripts/', '-t', './docs/source/_templates', '-d1', '-feMT', PATH,
    # ]))
    # app.connect('builder-inited', lambda a: apidoc.main([
    #     '-o', './docs/source/api', './nakecdysis/',
    # ]) if a else next)
    # sphinx-apidoc -o ./source/scripts/ -t ./source/_templates/ -feM ../library/
