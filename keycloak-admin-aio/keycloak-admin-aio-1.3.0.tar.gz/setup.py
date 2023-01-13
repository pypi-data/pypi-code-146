# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keycloak_admin_aio',
 'keycloak_admin_aio._resources',
 'keycloak_admin_aio._resources.admin_events',
 'keycloak_admin_aio._resources.attack_detection',
 'keycloak_admin_aio._resources.attack_detection.brute_force',
 'keycloak_admin_aio._resources.attack_detection.brute_force.users',
 'keycloak_admin_aio._resources.attack_detection.brute_force.users.by_id',
 'keycloak_admin_aio._resources.authentication',
 'keycloak_admin_aio._resources.authentication.required_actions',
 'keycloak_admin_aio._resources.client_scopes',
 'keycloak_admin_aio._resources.client_scopes.by_id',
 'keycloak_admin_aio._resources.client_scopes.by_id.scope_mappings',
 'keycloak_admin_aio._resources.client_scopes.by_id.scope_mappings.realm',
 'keycloak_admin_aio._resources.clients',
 'keycloak_admin_aio._resources.clients.by_id',
 'keycloak_admin_aio._resources.clients.by_id.default_client_scopes',
 'keycloak_admin_aio._resources.clients.by_id.default_client_scopes.by_id',
 'keycloak_admin_aio._resources.clients.by_id.user_sessions',
 'keycloak_admin_aio._resources.groups',
 'keycloak_admin_aio._resources.groups.by_id',
 'keycloak_admin_aio._resources.groups.by_id.children',
 'keycloak_admin_aio._resources.groups.by_id.members',
 'keycloak_admin_aio._resources.roles',
 'keycloak_admin_aio._resources.roles.by_id',
 'keycloak_admin_aio._resources.roles.by_id.composites',
 'keycloak_admin_aio._resources.roles.by_name',
 'keycloak_admin_aio._resources.roles.by_name.composites',
 'keycloak_admin_aio._resources.sessions',
 'keycloak_admin_aio._resources.sessions.by_id',
 'keycloak_admin_aio._resources.users',
 'keycloak_admin_aio._resources.users.by_id',
 'keycloak_admin_aio._resources.users.by_id.execute_actions_email',
 'keycloak_admin_aio._resources.users.by_id.groups',
 'keycloak_admin_aio._resources.users.by_id.groups.by_id',
 'keycloak_admin_aio._resources.users.by_id.role_mappings',
 'keycloak_admin_aio._resources.users.by_id.role_mappings.realm',
 'keycloak_admin_aio.types']

package_data = \
{'': ['*'], 'keycloak_admin_aio': ['_lib/*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'httpx>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'keycloak-admin-aio',
    'version': '1.3.0',
    'description': 'async keycloak admin api wrapper',
    'long_description': 'What is keycloak_admin_aio?\n---------------------------\n\nThis package provides an asynchronous api wrapper for the `keycloak admin api\n<https://www.keycloak.org/docs-api/15.0/rest-api>`_.\n\nThe main dependencies are:\n\n- `httpx <https://github.com/encode/httpx/>`_: asynchronous http client\n- `dacite <https://github.com/konradhalas/dacite>`_: parse nested dictionaries into nested dataclasses\n\nLinks:\n\n- `Source code <https://github.com/delphai/keycloak-admin-aio>`_\n- `Documentation <https://delphai.github.io/keycloak-admin-aio/>`_\n- `Pypi <https://pypi.org/project/keycloak-admin-aio/>`_\n\nHow to install?\n---------------\n\n.. code:: shell\n\n   poetry add keycloak-admin-aio\n\nHow to use it?\n--------------\n\n.. code:: python\n\n    import asyncio\n    from keycloak_admin_aio import KeycloakAdmin\n\n    server_url = "http://localhost:8080/auth"\n    client_id = "admin-cli"  # used by default\n    realm = "master"  # used by default\n\nWith administrator username and password:\n\n.. code:: python\n\n    keycloak_admin_args = {\n        "server_url": server_url,\n        "client_id": client_id,\n        "realm": realm,\n        "username": "admin",\n        "password": "password123",\n    }\n\n    async def main():\n        async with KeycloakAdmin.with_password(**keycloak_admin_args) as kc:\n            users = await kc.users.get(email="@google")\n            await asyncio.gather(\n                *[\n                    kc.users.by_id(user.id).execute_actions_email.send_email(\n                        ["UPDATE_PASSWORD"]\n                    )\n                    for user in users\n                ]\n            )\n\n    asyncio.run(main())\n\nWith client credentials:\n\n.. code:: python\n\n    keycloak_admin_args = {\n        "realm": realm,\n        "server_url": server_url,\n        "client_id": client_id,\n        "client_secret": "the_secret",\n    }\n\n    async def main():\n        async with KeycloakAdmin.with_client_credentials(**keycloak_admin_args) as kc:\n            ...\n\n    asyncio.run(main())\n\nLicense\n-------\n\n`Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_\n\n\n© Copyright 2021, delphai by AtomLeap GmbH\n',
    'author': 'Nicklas Sedlock',
    'author_email': 'nicklas@delphai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/delphai/keycloak-admin-aio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
