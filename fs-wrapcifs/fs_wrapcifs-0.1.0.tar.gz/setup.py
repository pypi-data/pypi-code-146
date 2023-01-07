# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fs', 'fs.wrapcifs']

package_data = \
{'': ['*']}

install_requires = \
['fs>=2.4.16,<3.0.0']

setup_kwargs = {
    'name': 'fs-wrapcifs',
    'version': '0.1.0',
    'description': 'Pyfilesystem2 wrapper for case insensitive access to a filesystem',
    'long_description': "fs.wrapcifs\n===========\n\n``fs.wrapcifs`` is a PyFileSystem2 wrapper which makes path lookups case insensitive.\n\nSupported Python versions\n-------------------------\n\n- Python 3.11\n\nUsage\n-----\n\n.. code:: python\n\n    >>> from fs.wrapcifs import WrapCaseInsensitive\n    >>> from fs.zipfs import ReadZipFS\n\n    >>> WrapCaseInsensitive(ReadZipFS('example.zip')).getinfo('abc').name == 'ABC'\n    ....\n    True\n\nLicense\n-------\n\nThis module is published under the MIT license.",
    'author': 'Omni Flux',
    'author_email': 'omniflux@omniflux.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Omniflux/fs.wrapcifs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11',
}


setup(**setup_kwargs)
