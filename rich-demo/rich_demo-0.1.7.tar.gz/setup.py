# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_demo']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.0.1,<14.0.0']

entry_points = \
{'console_scripts': ['rich-demo = rich_demo.__main__:run'],
 'pipx.run': ['rich-demo = rich_demo.__main__:run']}

setup_kwargs = {
    'name': 'rich-demo',
    'version': '0.1.7',
    'description': 'Tool to check the graphic features of a terminal using the rich library.',
    'long_description': '# Rich demo\n\nTool to check the graphic features of a terminal using the [rich library][1].\n\nIt can be used with [pipx][2]\n\n```bash\npipx run rich-demo\n```\n\nAlso, you can install it:\n\n```bash\npipx install rich-demo\nrich-demo\n```\n\n## Example\n\n-----\n\n![Rich-demo screenshot][3]\n\n-----\n\n[1]: https://github.com/Textualize/rich\n[2]: https://github.com/pypa/pipx\n[3]: https://github.com/chemacortes/rich-demo/raw/main/mintty_tiAfx8nc4v.png\n',
    'author': 'Chema Cortés',
    'author_email': 'dextrem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chemacortes/rich-demo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
