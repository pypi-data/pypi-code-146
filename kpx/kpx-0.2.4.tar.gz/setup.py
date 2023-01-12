# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['kpx']
install_requires = \
['boto3>=1.26,<2.0',
 'configparser>=5.3.0,<6.0.0',
 'prettytable>=3.5.0,<4.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['kpx = kpx:app']}

setup_kwargs = {
    'name': 'kpx',
    'version': '0.2.4',
    'description': 'CLI tool for AWS configuration files and quick interogations to AWS API',
    'long_description': '[![pipeline status](https://gitlab.com/kisphp/python-cli-tool/badges/main/pipeline.svg)](https://gitlab.com/kisphp/python-cli-tool/-/commits/main)\n[![coverage report](https://gitlab.com/kisphp/python-cli-tool/badges/main/coverage.svg)](https://gitlab.com/kisphp/python-cli-tool/-/commits/main)\n[![Latest Release](https://gitlab.com/kisphp/python-cli-tool/-/badges/release.svg)](https://gitlab.com/kisphp/python-cli-tool/-/releases)\n\n## Install\n\n```bash\n# Install or update it from pip\npip install -U kpx\n\n# Install or update it from gitlab\npip install -U kpx --index-url https://gitlab.com/api/v4/projects/24038501/packages/pypi/simple\n```\n\n\n## Usage\n\n```bash\n# Configure profile region and output type\nkpx conf [profile-name] [aws-zone] [output-type]\n\n# Configure profile credentials\nkpx cred [profile-name] [access-key-id] [secret-access-key]\n\n# List route53 hosted zones\nkpx r53\n\n# List records in a hosted zone\nkpx r53 [zone-id]\n\n# List ec2 instances (without pagination)\nkpx ec2\n```\n',
    'author': 'Bogdan Rizac',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
