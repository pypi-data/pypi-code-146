# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baseblock']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0', 'cryptography==38.0.1', 'unicodedata2']

setup_kwargs = {
    'name': 'baseblock',
    'version': '0.1.46',
    'description': 'Base Block of Common Enterprise Python Utilities',
    'long_description': '# Base Block (baseblock)\n\nBase Block of Common Enterprise Python Utilities\n\n\n## Crypto Base\nUsage\n```python\nfrom baseblock import CryptoBase\n\nkey = CryptoBase.generate_private_key()\n```\n\nThe `key` is used to both encrypt and decrypt text, like this:\n```python\ninput_text = "Hello, World!"\n\ncrypt = CryptoBase(key)\n\nx = crypt.encrypt_str(input_text)\ny = crypt.decrypt_str(x)\n\nassert input_text == y\n```\n\nThe key can also be stored in the environment under **BASEBLOCK_CRYPTO_KEY**.\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/climate-bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
