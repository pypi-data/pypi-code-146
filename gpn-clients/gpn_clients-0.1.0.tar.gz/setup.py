# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpn_clients',
 'gpn_clients.clients.nsi.v1',
 'gpn_clients.core',
 'gpn_clients.models',
 'gpn_clients.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'setuptools>=65.7.0,<66.0.0']

setup_kwargs = {
    'name': 'gpn-clients',
    'version': '0.1.0',
    'description': '',
    'long_description': '# 🀣 🅖🅟🅝 🅲🅻🅸🅴🅽🆃🆂 🀣 \n\nThis repository contains the source code for the GPN clients.\n\n## Poetry Setup\n\n```bash\npoetry config settings.virtualenvs.in-project true\n```\n',
    'author': 'Chumakov Mikhail Dmitrievich',
    'author_email': 'i@m-chumakov-dev.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
