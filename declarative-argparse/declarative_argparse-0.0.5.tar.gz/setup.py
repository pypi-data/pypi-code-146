# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['declarative_argparse', 'declarative_argparse.options']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'declarative-argparse',
    'version': '0.0.5',
    'description': 'A simple wrapper around argparse to permit declarative construction and argument retrieval.',
    'long_description': "# Declarative Argparse\n\nThis project introduces a wrapper argound the built-in `argparse` module that permits one to make a declarative parser for options.\n\n[[_TOC_]]\n\n## Example\n\n```python\nimport argparse\nfrom declarative_argparse import DeclarativeOptionParser\nfrom declarative_argparse.options.int import IntDO\nfrom declarative_argparse.options.str import StrDO\nclass DAPExample(DeclarativeOptionParser):\n    def __init__(self) -> None:\n        super().__init__(argp=argparse.ArgumentParser())\n        self.x: IntDO = self.addInt('--x', '-x', description='X coordinate')\n        self.y: IntDO = self.addInt('--y', '-y', description='Y coordinate')\n        self.name: StrDO = self.addStr('--name', description='Change tile name').setNArgs('?')\n        self.id: StrDO = self.addStr('id', description='specify tile ID')\n\n# ...\n\nargs = DAPExample()\nargs.parseArguments(['--x=0', '-y', '1', 'abc1'])\nassert args.x.get_value() == 0\nassert args.y.get_value() == 1\nassert args.name.get_value() is None\nassert args.id.get_value() == 'abc1'\n```\n\n## License\n\nMIT\n\nContributions are always welcome.",
    'author': 'Rob Nelson',
    'author_email': 'nexisentertainment@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/N3X15/declarative_argparse',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
