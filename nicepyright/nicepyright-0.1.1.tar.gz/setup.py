# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicepyright']

package_data = \
{'': ['*']}

install_requires = \
['parse>=1.19.0,<2.0.0', 'pyright>=1.1.288,<2.0.0', 'rich>=13.0.1,<14.0.0']

entry_points = \
{'console_scripts': ['nicepyright = nicepyright.main:watch']}

setup_kwargs = {
    'name': 'nicepyright',
    'version': '0.1.1',
    'description': '',
    'long_description': '## nicepyright\n\nnicepyright is a tool that provides a nicer CLI interface to the pyright type checker. It continuously monitors and displays type warnings in a more user-friendly format.\n\nPlease note that nicepyright is currently in an early stage of development, so it may be feature incomplete and contain bugs. However, it is already useful and can help you to find type warnings in your code faster and more easily.\n\n### Installation\n\n`nicepyright` is available on PyPI and can be installed with `pip`, `poetry`, or your favorite Python package manager.\n\n```bash\npoetry add --dev nicepyright\n```\n\n### Usage\n\nTo use nicepyright, navigate to the root directory of your project and run the following command:\n\n```bash\nnicepyright\n```\n\nMake sure that the environment being used is the one that contains all the libraries your project uses.\nThat is, if you are using a virtual environment, make sure that it is activated.\nIf you are using `poetry`, you can use the `poetry run` command to ensure that the correct version of `nicepyright` is used.\n\n```bash\npoetry run nicepyright\n```\n\nThis will start the pyright type checker and display the type warnings in a more user-friendly format.\n\n',
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
