# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['selenium_tkit']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent>=1.1.1,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'retimer>=0.1.0.9,<0.2.0.0',
 'selenium>=4.7.2,<5.0.0',
 'undetected-chromedriver>=3.1.7,<4.0.0',
 'webdriver-manager>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'selenium-tkit',
    'version': '0.1.0.1',
    'description': 'Another selenium toolkit',
    'long_description': "# selenium_tkit\n\n> This package is under development, it should be used with that in mind, not every system may be compatible\n\n[![PyPI version][pypi-image]][pypi-url]\n[![GitHub stars][stars-image]][stars-url]\n[![Support Python versions][versions-image]][versions-url]\n\n\n\n## Getting started\n\nYou can [get `selenium_tkit` from PyPI](https://pypi.org/project/selenium_tkit),\nwhich means it's easily installable with `pip`:\n\n```bash\npython -m pip install selenium_tkit\n```\n\n\n## Example usage\n\n```python\n```\n\n\n\n## Changelog\n\nRefer to the [CHANGELOG.md](https://github.com/henriquelino/selenium_tkit/blob/main/CHANGELOG.md) file.\n\n\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/selenium_tkit\n[pypi-url]: https://pypi.org/project/selenium_tkit/\n\n\n[stars-image]: https://img.shields.io/github/stars/henriquelino/selenium_tkit\n[stars-url]: https://github.com/henriquelino/selenium_tkit\n\n[versions-image]: https://img.shields.io/pypi/pyversions/selenium_tkit\n[versions-url]: https://pypi.org/project/selenium_tkit/\n\n",
    'author': 'henrique lino',
    'author_email': 'henrique.lino97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
