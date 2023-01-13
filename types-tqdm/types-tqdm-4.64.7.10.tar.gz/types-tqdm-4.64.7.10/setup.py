from setuptools import setup

name = "types-tqdm"
description = "Typing stubs for tqdm"
long_description = '''
## Typing stubs for tqdm

This is a PEP 561 type stub package for the `tqdm` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`tqdm`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/tqdm. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `b216053432bffa2aef13c33b8aec50836e4b6935`.
'''.lstrip()

setup(name=name,
      version="4.64.7.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tqdm.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['tqdm-stubs'],
      package_data={'tqdm-stubs': ['__init__.pyi', '_dist_ver.pyi', '_main.pyi', '_monitor.pyi', '_tqdm.pyi', '_tqdm_gui.pyi', '_tqdm_notebook.pyi', '_tqdm_pandas.pyi', '_utils.pyi', 'asyncio.pyi', 'auto.pyi', 'autonotebook.pyi', 'cli.pyi', 'contrib/__init__.pyi', 'contrib/bells.pyi', 'contrib/concurrent.pyi', 'contrib/discord.pyi', 'contrib/itertools.pyi', 'contrib/logging.pyi', 'contrib/slack.pyi', 'contrib/telegram.pyi', 'contrib/utils_worker.pyi', 'dask.pyi', 'gui.pyi', 'keras.pyi', 'notebook.pyi', 'rich.pyi', 'std.pyi', 'tk.pyi', 'utils.pyi', 'version.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
