# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conceptionlogicielletp2']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy==0.18.0', 'python-Levenshtein==0.20.9', 'python-dotenv==0.21.0']

setup_kwargs = {
    'name': 'conceptionlogicielletp2',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Hello world\n\nStart here :\n\n```\ngit clone https://gitlab.com/conception-logicielle/tp2-conception-corrige.git tp2\n```\n\nInstall requirements file :\n\n```\npoetry install\n```\n\nThen you can run the app :\n\n```\npoetry run python tp2\n```\n\n_on some operating systems, python you might have to use cmd python3 or python2_\n\nYou can change words using env variables\ne.g. on linux :\n\n```\nexport DEFAULT_MOT_UN=toto\n```\n\n_on some operating systems, python you might have to use cmd python3 or python2_\n\nYou can also download the package:\n\n```\npip install\n```\n',
    'author': 'ragatzino',
    'author_email': 'antoine.brunetti@insee.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
