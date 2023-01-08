from __future__ import annotations

import os
import sys
from typing import Any


# -- Project information --
project: str = "asyncakinator"
copyright: str = "2022, avizum"
author: str = "avizum"
release: str = "1.5.2"


# -- General Configuration --

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinxcontrib_trio",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

exclude_patters: list[str] = ["_build", "Thumbs.db", ".DS_Store"]

needs_sphinx: str = "5.1.1"
nitpicky: bool = True


# -- Options for HTML output --

html_theme: str = "furo"

html_title: str = "asyncakinator"

html_css_files: list[str] = [
    "custom.css",
]
html_static_path: list[str] = ["static"]


# -- Extensions --
autoclass_content: str = "class"
autodoc_class_signature: str = "mixed"
autodoc_member_order: str = "bysource"
autodoc_default_options: dict[str, Any] = {"undoc-members": True}
autodoc_typehints: str = "signature"
autodoc_type_aliases: dict[str, str] = {}
autodoc_typehints_format: str = "short"

intersphinx_mapping: dict[str, tuple[str, None]] = {
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
    "python": ("https://docs.python.org/3.10", None),
}

extlinks: dict[str, tuple[str, str]] = {}
extlinks_detect_hardcoded_links: bool = True
