# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scp_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.73,<2.0.0', 'pandas>=1.2.4,<2.0.0']

entry_points = \
{'console_scripts': ['scp-analyser = scp_analyzer:discover_scps.main',
                     'scp-analyzer = scp_analyzer:discover_scps.main']}

setup_kwargs = {
    'name': 'scp-analyzer',
    'version': '0.3.2',
    'description': 'Discover and present SCPs applicable to each account in an AWS Organization',
    'long_description': "# Service Control Policy Analyzer\n\nThis tool collects and presents all the Service Control Policies (SCPs) applicable to each account in an AWS Organization. It's purpose is to help developers and security teams understand how SCPs might be blocking activities in any account of the AWS Organization.\n\n## Sample output\n\n![scp-analyzeroutput](doc/sample-output.png)\n\n## Installation\n\n`pip install scp-analyzer` \n\n## Use\n\nObtain AWS CLI credentials to the Organizations Management account or a delegated administration account. Ensure you have Organizations Read Only permissions and run `scp-analyzer` to collect data. The tool will write output to a csv file.\n\n## Security\n\nSee [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.\n\n## License\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n\n\n",
    'author': 'Pedro Galvao',
    'author_email': 'pgalvao@amazon.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aws-samples/scp-analyzer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
