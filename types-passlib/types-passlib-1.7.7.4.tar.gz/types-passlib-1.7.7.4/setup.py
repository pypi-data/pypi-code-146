from setuptools import setup

name = "types-passlib"
description = "Typing stubs for passlib"
long_description = '''
## Typing stubs for passlib

This is a PEP 561 type stub package for the `passlib` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`passlib`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/passlib. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `b216053432bffa2aef13c33b8aec50836e4b6935`.
'''.lstrip()

setup(name=name,
      version="1.7.7.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/passlib.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['passlib-stubs'],
      package_data={'passlib-stubs': ['__init__.pyi', 'apache.pyi', 'apps.pyi', 'context.pyi', 'crypto/__init__.pyi', 'crypto/_blowfish/__init__.pyi', 'crypto/_blowfish/_gen_files.pyi', 'crypto/_blowfish/base.pyi', 'crypto/_blowfish/unrolled.pyi', 'crypto/_md4.pyi', 'crypto/des.pyi', 'crypto/digest.pyi', 'crypto/scrypt/__init__.pyi', 'crypto/scrypt/_builtin.pyi', 'crypto/scrypt/_gen_files.pyi', 'crypto/scrypt/_salsa.pyi', 'exc.pyi', 'ext/__init__.pyi', 'ext/django/__init__.pyi', 'ext/django/models.pyi', 'ext/django/utils.pyi', 'handlers/__init__.pyi', 'handlers/argon2.pyi', 'handlers/bcrypt.pyi', 'handlers/cisco.pyi', 'handlers/des_crypt.pyi', 'handlers/digests.pyi', 'handlers/django.pyi', 'handlers/fshp.pyi', 'handlers/ldap_digests.pyi', 'handlers/md5_crypt.pyi', 'handlers/misc.pyi', 'handlers/mssql.pyi', 'handlers/mysql.pyi', 'handlers/oracle.pyi', 'handlers/pbkdf2.pyi', 'handlers/phpass.pyi', 'handlers/postgres.pyi', 'handlers/roundup.pyi', 'handlers/scram.pyi', 'handlers/scrypt.pyi', 'handlers/sha1_crypt.pyi', 'handlers/sha2_crypt.pyi', 'handlers/sun_md5_crypt.pyi', 'handlers/windows.pyi', 'hash.pyi', 'hosts.pyi', 'ifc.pyi', 'pwd.pyi', 'registry.pyi', 'totp.pyi', 'utils/__init__.pyi', 'utils/binary.pyi', 'utils/compat/__init__.pyi', 'utils/compat/_ordered_dict.pyi', 'utils/decor.pyi', 'utils/des.pyi', 'utils/handlers.pyi', 'utils/md4.pyi', 'utils/pbkdf2.pyi', 'win32.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
