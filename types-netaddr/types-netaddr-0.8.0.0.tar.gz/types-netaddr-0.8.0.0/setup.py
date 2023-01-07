from setuptools import setup

name = "types-netaddr"
description = "Typing stubs for netaddr"
long_description = '''
## Typing stubs for netaddr

This is a PEP 561 type stub package for the `netaddr` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `netaddr`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/netaddr. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `2c9816e7888a8ea550da436f4e3c70af00346d56`.
'''.lstrip()

setup(name=name,
      version="0.8.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/netaddr.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['netaddr-stubs'],
      package_data={'netaddr-stubs': ['__init__.pyi', 'cli.pyi', 'compat.pyi', 'contrib/__init__.pyi', 'contrib/subnet_splitter.pyi', 'core.pyi', 'eui/__init__.pyi', 'eui/ieee.pyi', 'fbsocket.pyi', 'ip/__init__.pyi', 'ip/glob.pyi', 'ip/iana.pyi', 'ip/nmap.pyi', 'ip/rfc1924.pyi', 'ip/sets.pyi', 'strategy/__init__.pyi', 'strategy/eui48.pyi', 'strategy/eui64.pyi', 'strategy/ipv4.pyi', 'strategy/ipv6.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
