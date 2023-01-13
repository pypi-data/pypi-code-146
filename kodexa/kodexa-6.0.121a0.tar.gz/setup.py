# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kodexa',
 'kodexa.assistant',
 'kodexa.cli',
 'kodexa.connectors',
 'kodexa.model',
 'kodexa.pipeline',
 'kodexa.platform',
 'kodexa.selectors',
 'kodexa.steps',
 'kodexa.testing',
 'kodexa.training']

package_data = \
{'': ['*'], 'kodexa.cli': ['templates/*']}

install_requires = \
['addict==2.4.0',
 'appdirs>=1.4.4,<2.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'click==8.1.3',
 'datamodel-code-generator>=0.13.0,<0.14.0',
 'deepdiff==5.8.1',
 'flake8>=6.0.0,<7.0.0',
 'jq==1.2.2',
 'jsonpickle==2.2.0',
 'mkdocs-material>=9.0.3,<10.0.0',
 'msgpack==1.0.4',
 'mypy>=0.991,<0.992',
 'pandas==1.4.3',
 'ply>=3.11,<4.0',
 'pydantic-yaml>=0.8.0,<0.9.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyfunctional>=1.4.3,<1.5.0',
 'pytest-runner==6.0.0',
 'pytest==7.1.2',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'rich==12.5.1',
 'simpleeval==0.9.12',
 'texttable>=1.6.7,<2.0.0',
 'twine==4.0.1',
 'urllib3>=1.26.14,<2.0.0',
 'wheel==0.38.1']

setup_kwargs = {
    'name': 'kodexa',
    'version': '6.0.121a0',
    'description': '',
    'long_description': '# Kodexa\n\n![Build](https://github.com/kodexa-ai/kodexa/workflows/Python%20Package%20Using%20Anaconda/badge.svg)\n\nKodexa is designed to allow you to work with a wide range of unstructured and semi-structured content and enables you to work with the Kodexa Platform.\n\n## Documentation & Examples\n\nDocumentation is available on [Github](https://docs.kodexa.com)\n\nFor more information on how to use Kodexa see https://www.kodexa.com/\n\n## Current Development\n\nThe main branch is 6.0 which is a production release.\n\n## Set-up\n\nEnsure you have Anaconda 3 or greater installed, then run:\n\n    conda env create -f environment.yml \n\nActivate the conda environment with the command:\n\n    conda activate kodexa\n    pip install -r requirements.txt\n\n## License\n\nApache 2.0\n',
    'author': 'Austin Redenbaugh',
    'author_email': '43683341+AustinRedenbaugh@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
