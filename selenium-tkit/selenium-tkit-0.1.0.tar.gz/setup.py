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
    'version': '0.1.0',
    'description': 'Another selenium toolkit',
    'long_description': '',
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
