# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hyperscan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hyperscan',
    'version': '0.3.3',
    'description': 'Python bindings for Hyperscan.',
    'long_description': "# Hyperscan for Python\n\n![python-hyperscan workflow](https://github.com/darvid/python-hyperscan/workflows/python-hyperscan%20workflow/badge.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hyperscan.svg)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/hyperscan.svg)\n![PyPI - Status](https://img.shields.io/pypi/status/hyperscan.svg)\n![PyPI - License](https://img.shields.io/pypi/l/hyperscan.svg)\n[![Read the Docs](https://img.shields.io/readthedocs/python-hyperscan.svg)](https://python-hyperscan.readthedocs.io/en/latest/)\n\nA CPython extension for [Hyperscan](https://www.hyperscan.io/), Intel's\nopen source, high-performance multiple regex matching library. Currently\nonly supports manylinux-compatible Linux distributions.\n\n## Installation\n\n```shell\npip install hyperscan\n```\n\n## API Support\n\n``python-hyperscan`` currently exposes *most* of the C API, with the\nfollowing caveats or exceptions:\n\n* No [stream compression][2] support.\n* No [custom allocator][3] support.\n* ``hs_expression_info``, ``hs_expression_ext_info``,\n  ``hs_populate_platform``, and ``hs_serialized_database_info`` not\n  exposed yet.\n\n✨ As of v0.3.0, ``python-hyperscan`` statically links against Hyperscan,\nso having the library installed on your system is not required. Prior\nversions of ``python-hyperscan`` require Hyperscan v5.2 or newer. ✨\n\nBuilding from source requires Hyperscan compiled and installed with the\nfollowing CMake flags set:\n\n* ``FAT_RUNTIME=OFF``\n* ``BUILD_STATIC_AND_SHARED=ON`` *only if* ``BUILD_SHARED_LIBS`` is also\n  on, in the event there are other applications colocated with\n  ``python-hyperscan`` that need the shared libraries. Otherwise ignore\n  this flag, as by default Hyperscan will build static libraries.\n* ``CMAKE_C_FLAGS`` and ``CMAKE_CXX_FLAGS`` set to ``-fPIC``\n\nSee the [documentation][6] for more detailed build instructions.\n\n## Resources\n\n* [PyPI Project](https://pypi.org/project/hyperscan/)\n* [Documentation][6]\n* [Hyperscan C API Documentation](http://intel.github.io/hyperscan/dev-reference/)\n\n[1]: http://intel.github.io/hyperscan/dev-reference/chimera.html\n[2]: http://intel.github.io/hyperscan/dev-reference/runtime.html#stream-compression\n[3]: http://intel.github.io/hyperscan/dev-reference/runtime.html#custom-allocators\n[4]: http://intel.github.io/hyperscan/dev-reference/compilation.html\n[5]: https://github.com/darvid/python-hyperscan/issues\n[6]: https://python-hyperscan.readthedocs.io\n",
    'author': 'David Gidwani',
    'author_email': 'david.gidwani@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/darvid/python-hyperscan',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
