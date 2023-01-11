from setuptools import setup

name = "types-python-datemath"
description = "Typing stubs for python-datemath"
long_description = '''
## Typing stubs for python-datemath

This is a PEP 561 type stub package for the `python-datemath` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-datemath`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-datemath. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `28bf5c9ddd7961cb2f7d46eb29b470b06b3d16aa`.
'''.lstrip()

setup(name=name,
      version="1.5.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-datemath.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['arrow>=1.0.1'],
      packages=['datemath-stubs'],
      package_data={'datemath-stubs': ['__init__.pyi', 'helpers.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
