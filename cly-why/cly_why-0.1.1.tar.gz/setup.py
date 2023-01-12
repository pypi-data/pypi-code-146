# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cly_why']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cly-why',
    'version': '0.1.1',
    'description': 'A super simple functional cli helper lib',
    'long_description': "# Why?\nI wanted a simple library to write small to moderate cli programs\n\n# Why not X?\n## X = argparse\nIts way more then what I need 99% of the time.\n\n## X = click\nI don't particularly like decorators.\n\n## X = typer\nI've used typer a bit, but it never clicked with me.\n\n# Feature List\n- [ ] Tests\n- [X] Colorize and Text Decorate\n- [ ] \n- [ ] \n",
    'author': '00il',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
