# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ivyorm',
 'ivyorm.module',
 'ivyorm.module.connection',
 'ivyorm.module.connectors',
 'ivyorm.module.interface',
 'ivyorm.module.util']

package_data = \
{'': ['*'],
 'ivyorm': ['ivypy.egg-info/*', 'model/*'],
 'ivyorm.module': ['connectors/keys/*']}

setup_kwargs = {
    'name': 'ivyorm',
    'version': '0.1.1',
    'description': 'An ORM for Python',
    'long_description': '# article i followed for creating a package\nhttps://mathspp.com/blog/how-to-create-a-python-package-in-2022\n\n# first, we need pipx in order to install poetry\npython -m pip install --user pipx\n\n# make sure the right python scripts folder is in the PATH env varaible on windows\n\npipx install poetry\n\n#update the PATH env\npipx ensurepath\n\n# reload the shell\n\n# for a new project, run \'poetry new .\' in the new empty directory\n# for an existing project, type the below in the the directory and follow the prompts\npoetry init\n\n# now run install\npoetry install\n\n# do the git stuff if a new project that\'s not on git yet\ngit init\ngit add *\ngit commit -m "First commit"\ngit branch -M main\ngit remote add origin https://github.com/JamesRandell/ivypy.git\ngit push -u origin main\n\n# more poetry stuff \npoetry add -D pre-commit\n\npoetry config repositories.testpypi https://test.pypi.org/legacy/\n\n\n#api token\n\n# test account\npoetry config http-basic.testpypi __token__ test-token-here\n\npoetry build\npoetry publish -r testpypi\n\n# live account\npoetry config pypi-token.pypi live-token-here\n\n\npoetry publish --build\n',
    'author': 'James Randell',
    'author_email': 'jamesrandell@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
