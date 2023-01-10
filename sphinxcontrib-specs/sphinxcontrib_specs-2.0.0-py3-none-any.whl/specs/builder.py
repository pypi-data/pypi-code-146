"""sphinxcontrib.specs.builder

The Specializations builder.
"""

import warnings

from sphinx.builders.html import StandaloneHTMLBuilder


class SpecsBuilder(StandaloneHTMLBuilder):
    name = "specs"
    search = False

    def init(self) -> None:
        warnings.warn(
            "SpecsBuilder is deprecated. Use a built-in HTML builder instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return super().init()
