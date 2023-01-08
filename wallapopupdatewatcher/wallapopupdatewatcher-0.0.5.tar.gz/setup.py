# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wallapopupdatewatcher']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'wallapopupdatewatcher',
    'version': '0.0.5',
    'description': 'A library to watch for new items at wallapop.es',
    'long_description': '# Wallapop update notifier\n\n### This package can be use to provide updates when new products appear on Wallapop. Install it just by using:<br><br>\n`pip install wallapopUpdateWatcher`\n### Basic usage example\n```python\nfrom wallapopUpdateWatcher import updateWatcher,Query,Producto\nimport asyncio\nasync def callback(q: Query, l: list[Producto])\n    for prod in producto:\n        print(q.msg())\n\n\nasync def main()\n    watcher = wallapopUpdateWatcher(callback)\n    await watcher.create("Keywords",(15,30))\n    # this creates a search for the product "Keywords"\n    # between 15€ and 30€. \n\n    while(True):\n        await watcher.checkOperation()\n        await asyncio.sleep(5)\n\nasyncio.run(main())\n```\n',
    'author': 'Adair-GA',
    'author_email': 'adairyves@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
