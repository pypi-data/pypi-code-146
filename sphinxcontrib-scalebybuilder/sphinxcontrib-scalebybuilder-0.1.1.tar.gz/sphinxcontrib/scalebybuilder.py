# -*- coding: utf-8 -*-
"""
    sphinxcontrib.scalebybuilder
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Set scaling factor of images and figures depending on the builder.

    :copyright: Copyright 2018-2023 by Stefan Wiehler
                <sphinx_contribute@missinglinkelectronics.com>.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import images

from sphinx.transforms import SphinxTransform
from sphinx.util import logging

if False:
    # For type annotation
    from typing import Any, Dict  # NOQA
    from sphinx.application import Sphinx  # NOQA


logger = logging.getLogger(__name__)


class ImageScaledByBuilder(images.Image):
    option_spec = images.Image.option_spec.copy()


class FigureScaledByBuilder(images.Figure):
    option_spec = images.Figure.option_spec.copy()


class ScaleByBuilder(SphinxTransform):
    default_priority = 410

    def apply(self):
        # type: () -> None
        for node in self.document.traverse(nodes.image):
            builder_name = self.app.builder.name
            if 'scale-' + builder_name in node:
                node['scale'] = node['scale-' + builder_name]


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    for builder_name in app.registry.builders.keys():
        scale = 'scale-' + builder_name
        ImageScaledByBuilder.option_spec[scale] = directives.percentage
        FigureScaledByBuilder.option_spec[scale] = directives.percentage
    directives.register_directive('image', ImageScaledByBuilder)
    directives.register_directive('figure', FigureScaledByBuilder)
    app.add_post_transform(ScaleByBuilder)

    return {'version': '0.1.0', 'parallel_read_safe': True}
