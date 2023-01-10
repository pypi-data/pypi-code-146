# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cloud_connectors',
 'cloud_connectors.aws_connector',
 'cloud_connectors.azure_connector',
 'cloud_connectors.common',
 'cloud_connectors.common.cli',
 'cloud_connectors.common.cli.commands',
 'cloud_connectors.common.plugins',
 'cloud_connectors.gcp_connector',
 'cloud_connectors.plugins']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'backoff>=2.1.2,<3.0.0',
 'censys>=2.1.8,<3.0.0',
 'inquirerpy>=0.3.3,<0.4.0',
 'pydantic[dotenv,email]>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['censys-cc = censys.cloud_connectors.common.cli:main']}

setup_kwargs = {
    'name': 'censys-cloud-connectors',
    'version': '3.1.0b2',
    'description': 'The Censys Unified Cloud Connector is a standalone connector that gathers assets from various cloud providers and stores them in Censys ASM.',
    'long_description': '# Censys Unified Cloud Connector\n\n[![GitHub release (latest by date)](https://img.shields.io/github/v/release/censys/censys-cloud-connector)][github]\n[![PyPI - License](https://img.shields.io/pypi/l/censys-cloud-connectors)][license]\n[![AWS Supported](https://img.shields.io/badge/-Supported-orange?logo=amazonaws)][aws]\n[![Azure Supported](https://img.shields.io/badge/-Supported-green?logo=microsoftazure)][azure]\n[![GCP Supported](https://img.shields.io/badge/-Supported-blue?logo=googlecloud&logoColor=white)][gcp]\n\nThe Censys Unified Cloud Connector is a standalone connector that gathers\nassets from various cloud providers and stores them in Censys ASM. This\nConnector offers users the ability to supercharge our ASM Platform with total\ncloud visibility. This connector currently supports the following cloud\nproviders: AWS, Azure, and GCP. Please see our\n[supported providers][supported-providers].\n\n## Documentation\n\nPlease view our documentation on [Read the Docs][censys-cloud-connector-docs].\n\n## Developer Documentation\n\nAll contributions (no matter how small) are always welcome. See\n[Contributing to the Cloud Connector][contributing] to change or\ntest the code or for information on the CI/CD pipeline.\n\n## License\n\nThis software is licensed under [Apache License, Version 2.0][license].\n\n- Copyright (C) 2022 Censys, Inc.\n\n<!-- References -->\n\n[aws]: https://censys-cloud-connector.readthedocs.io/en/stable/providers.html#amazon-web-services\n[azure]: https://censys-cloud-connector.readthedocs.io/en/stable/providers.html#azure-cloud\n[censys-cloud-connector-docs]: https://censys-cloud-connector.readthedocs.io/en/stable/\n[contributing]: https://github.com/censys/censys-cloud-connector/tree/main/CONTRIBUTING.md\n[gcp]: https://censys-cloud-connector.readthedocs.io/en/stable/providers.html#google-cloud-platform\n[github]: https://github.com/censys/censys-cloud-connector\n[license]: http://www.apache.org/licenses/LICENSE-2.0\n[supported-providers]: https://censys-cloud-connector.readthedocs.io/en/stable/providers.html\n',
    'author': 'Censys, Inc.',
    'author_email': 'support@censys.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
