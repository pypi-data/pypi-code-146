# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptal_api',
 'ptal_api.core.values',
 'ptal_api.providers',
 'ptal_api.schema',
 'ptal_api.tdm_builder']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core==3.2.3', 'python-keycloak==2.6.0', 'sgqlc==16.0']

setup_kwargs = {
    'name': 'ptal-api',
    'version': '0.10.10',
    'description': 'TALISMAN API adapter',
    'long_description': "# ptal-api\n\nPython adapter for Talisman-based app\n\nHow to create trivial adapter:\n\n    graphql_url = 'https://demo.talisman.ispras.ru/graphql' # or another talisman-based app\n    auth_url = 'https://demo.talisman.ispras.ru/auth/'\n    realm = 'demo'\n    client_id = 'web-ui'\n    client_secret = '<some-secret>'\n\n    gql_client = KeycloakAwareGQLClient(\n        graphql_url, 10000, 5,\n        auth_url=auth_url,\n        realm=realm, client_id=client_id, user='admin', pwd='admin',\n        client_secret=client_secret\n    ).__enter__()\n\n    adapter = TalismanAPIAdapter(gql_client, {})\n\n    c = adapter.get_concept('ОК-123456')\n",
    'author': 'Evgeny Bechkalo',
    'author_email': 'bechkalo@ispras.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
