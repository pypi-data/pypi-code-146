# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyveb']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.24.24',
 'numpy==1.21.2',
 'pandas==1.3.2',
 'psutil>=5.9.0,<6.0.0',
 'psycopg2-binary==2.9.1',
 'pyarrow==5.0.0',
 'pyodbc==4.0.30',
 'pyspark>=3.0.0,<4.0.0',
 'pyyaml==6.0',
 'requests==2.27.1',
 's3fs==0.4.2',
 'selenium>=4.5.0,<5.0.0',
 'simple-ddl-parser==0.26.5',
 'webdriver-manager==3.4.1',
 'xlrd>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pyveb',
    'version': '0.1.79',
    'description': 'Package containing common code and reusable components for pipelines and dags',
    'long_description': '# General \n\nPackage containing resuable code components for data pipelines and dags deployed to pypi.\n\n# Usage\n\nInstall/Upgrade locally: \n\n```\n$ pip3 install pyveb\n$ pip3 install pyveb --upgrade\n```\n\nImport in python\n\n```\nimport pyveb\nfrom pyveb import selenium_client\n```\n\n\n# Update package\n\nPackage is automaticly deployed to pypi via github actions. Just commit and open a pull request. During the action workflow, the version will be automatically bumped and updated pyproject.toml is commited back. \n\n! in case a dependency is added to pyproject.toml, no workflow is started unless there are also changes to src/pyveb/** \n\n\n\n\n\n\n\n\n\n',
    'author': 'pieter',
    'author_email': 'pieter.de.petter@veb.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
