# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pybaserepo']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'pybaserepo',
    'version': '0.2.1',
    'description': 'base repo config',
    'long_description': '# A sample Python project\n\nA sample project to copy the correct structure of a python project.\n\n## Pyproject.toml\nProject properties to update:\n* _name_ : name of the project\n* _description_ : description of the project\n* _authors_ : authors of the project\n* _keywords_ : keywords to help search of the project\n* _classifiers_ : one or more [classifiers](https://pypi.org/classifiers/) of the project\n* _dependencies_ : equivalent to requirements.txt\n* _urls_ : homepage, documentation and repository\n* _scripts_ : startup script when executing like **python -m < project >**\n* _tool.bumpver.file_pattern_ : name of the folder of the project\n\n## Update to PyPi\nSteps to update to pip:\n* _tox -r_ : check integrity of the project and execute tests\n* _bumpver update --patch_ : update version of the project. Also --minor and --major is supported\n* _python -m build_ : build the project\n* _twine check dist/*_ : check build files\n* _twine upload dist/*_ : upload to PyPi (may upload before to testpypi with _twine upload -r testpypi dist/*_)\n* _pip install < project >_ : to install the package and check it (may check before from testpypi with _pip install -i https://test.pypi.org/simple < project >_)\n\n# Structure\nData folder is used for external files (like configuration files or scripts)\n\nBasic packages to install: _pip install .[dev]_',
    'author': 'Ivan Lamperti',
    'author_email': 'ivan.lamperti.work@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
