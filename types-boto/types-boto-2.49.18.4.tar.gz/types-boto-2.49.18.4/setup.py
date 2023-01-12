from setuptools import setup

name = "types-boto"
description = "Typing stubs for boto"
long_description = '''
## Typing stubs for boto

This is a PEP 561 type stub package for the `boto` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`boto`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/boto. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `b9eab637cbac042e14016d5e4db10c140aeeffff`.
'''.lstrip()

setup(name=name,
      version="2.49.18.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/boto.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['boto-stubs'],
      package_data={'boto-stubs': ['__init__.pyi', 'auth.pyi', 'auth_handler.pyi', 'compat.pyi', 'connection.pyi', 'ec2/__init__.pyi', 'elb/__init__.pyi', 'exception.pyi', 'kms/__init__.pyi', 'kms/exceptions.pyi', 'kms/layer1.pyi', 'plugin.pyi', 'regioninfo.pyi', 's3/__init__.pyi', 's3/acl.pyi', 's3/bucket.pyi', 's3/bucketlistresultset.pyi', 's3/bucketlogging.pyi', 's3/connection.pyi', 's3/cors.pyi', 's3/deletemarker.pyi', 's3/key.pyi', 's3/keyfile.pyi', 's3/lifecycle.pyi', 's3/multidelete.pyi', 's3/multipart.pyi', 's3/prefix.pyi', 's3/tagging.pyi', 's3/user.pyi', 's3/website.pyi', 'utils.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
