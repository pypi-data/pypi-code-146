# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['store']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'babichjacob-store',
    'version': '0.2.0',
    'description': 'A Python implementation of svelte/store',
    'long_description': '<h1 align="center">💾 Store</h1>\n\nThis library is a Python implementation of `svelte/store`.\n\n## 💻 Installation\n\nThis package is [published to PyPI as `babichjacob-store`](https://pypi.org/project/babichjacob-store/).\n\n## 🛠 Usage\n\n```py\nfrom store import writable\n\nmy_store = writable(17)\nmy_store.subscribe(lambda value: print(f"Store value changed to {value}"))\nmy_store.set(23)\n\n# readable and derived are also available but I didn\'t feel like documenting them because this is just for myself\n```\n\n## 😵 Help! I have a question\n\nCreate an issue and I\'ll try to help.\n\n## 😡 Fix! There is something that needs improvement\n\nCreate an issue or pull request and I\'ll try to fix.\n\n## 📄 License\n\nMIT\n\n## 🙏 Attribution\n\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'J or Jacob Babich',
    'author_email': 'jacobbabichpublic+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/babichjacob/python-store',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
