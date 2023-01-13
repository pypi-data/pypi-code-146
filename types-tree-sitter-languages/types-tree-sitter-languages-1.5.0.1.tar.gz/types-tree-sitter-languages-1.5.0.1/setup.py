from setuptools import setup

name = "types-tree-sitter-languages"
description = "Typing stubs for tree-sitter-languages"
long_description = '''
## Typing stubs for tree-sitter-languages

This is a PEP 561 type stub package for the `tree-sitter-languages` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`tree-sitter-languages`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/tree-sitter-languages. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `194690745150e871c004111f0cccbbf5e0fd1568`.
'''.lstrip()

setup(name=name,
      version="1.5.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tree-sitter-languages.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-tree-sitter'],
      packages=['tree_sitter_languages-stubs'],
      package_data={'tree_sitter_languages-stubs': ['__init__.pyi', 'core.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
