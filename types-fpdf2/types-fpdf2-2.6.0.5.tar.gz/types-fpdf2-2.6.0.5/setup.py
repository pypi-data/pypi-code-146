from setuptools import setup

name = "types-fpdf2"
description = "Typing stubs for fpdf2"
long_description = '''
## Typing stubs for fpdf2

This is a PEP 561 type stub package for the `fpdf2` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`fpdf2`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/fpdf2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `ea0ae2155e8a04c9837903c3aff8dd5ad5f36ebc`.
'''.lstrip()

setup(name=name,
      version="2.6.0.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/fpdf2.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-Pillow'],
      packages=['fpdf-stubs'],
      package_data={'fpdf-stubs': ['__init__.pyi', 'actions.pyi', 'annotations.pyi', 'deprecation.pyi', 'drawing.pyi', 'enums.pyi', 'errors.pyi', 'fonts.pyi', 'fpdf.pyi', 'graphics_state.pyi', 'html.pyi', 'image_parsing.pyi', 'line_break.pyi', 'linearization.pyi', 'outline.pyi', 'output.pyi', 'prefs.pyi', 'recorder.pyi', 'sign.pyi', 'structure_tree.pyi', 'svg.pyi', 'syntax.pyi', 'template.pyi', 'transitions.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
