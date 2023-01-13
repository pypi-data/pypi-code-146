from setuptools import setup

name = "types-Flask-Migrate"
description = "Typing stubs for Flask-Migrate"
long_description = '''
## Typing stubs for Flask-Migrate

This is a PEP 561 type stub package for the `Flask-Migrate` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Flask-Migrate`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Flask-Migrate. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `9a76e5a66938e8a1f784116dcf32fa17a5e61ba1`.
'''.lstrip()

setup(name=name,
      version="4.0.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Flask-Migrate.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-Flask-SQLAlchemy', 'Flask>=2.0.0'],
      packages=['flask_migrate-stubs'],
      package_data={'flask_migrate-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
