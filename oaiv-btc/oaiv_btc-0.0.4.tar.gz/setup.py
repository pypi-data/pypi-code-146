#
import setuptools
from setuptools import setup


metadata = {'name': 'oaiv_btc',
            'maintainer': 'Edward Azizov',
            'maintainer_email': 'edazizovv@gmail.com',
            'description': 'BTC Blockchain Interaction Library',
            'license': 'MIT',
            'url': 'https://github.com/edazizovv/oaiv_btc',
            'download_url': 'https://github.com/edazizovv/oaiv_btc',
            'packages': setuptools.find_packages(),
            'include_package_data': True,
            'version': '0.0.4',
            'long_description': '',
            'python_requires': '>=3.10',
            'install_requires': []}

setup(**metadata)
