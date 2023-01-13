# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gungus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gungus',
    'version': '0.0.0',
    'description': '',
    'long_description': '# The GUNGUS Python library\n\n\n## License\nThis library is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis library is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this library.  If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'Cesar Perez',
    'author_email': 'ttyrho@gmail.com',
    'maintainer': 'Cesar Perez',
    'maintainer_email': 'ttyrho@gmail.com',
    'url': 'https://github.com/ttyrho/gungus',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
