# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_aiohttp_client']
install_requires = \
['aiohttp>=3.8.3,<4.0.0']

entry_points = \
{'pytest11': ['pytest_aiohttp_client = pytest_aiohttp_client']}

setup_kwargs = {
    'name': 'pytest-aiohttp-client',
    'version': '0.1.0',
    'description': 'Pytest `client` fixture for the Aiohttp',
    'long_description': '# pytest-aiohttp-client\n\nAwesome pytest fixture for awesome [aiohttp](https://docs.aiohttp.org/en/stable/)!\n\n[![test](https://github.com/sivakov512/pytest-aiohttp-client/workflows/test/badge.svg)](https://github.com/sivakov512/pytest-aiohttp-client/actions?query=workflow%3Atest)\n[![Coverage Status](https://coveralls.io/repos/github/sivakov512/pytest-aiohttp-client/badge.svg?branch=master)](https://coveralls.io/github/sivakov512/pytest-aiohttp-client?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Python versions](https://img.shields.io/pypi/pyversions/pytest-aiohttp-client.svg)](https://pypi.python.org/pypi/pytest-aiohttp-client)\n[![PyPi](https://img.shields.io/pypi/v/pytest-aiohttp-client.svg)](https://pypi.python.org/pypi/pytest-aiohttp-client)\n\n## Installation\n\nInstall it via `pip` tool:\n\n```bash\npip install pytest-aiohttp-client\n```\n\nor Poetry:\n\n```bash\npoetry add yandex-geocoder\n```\n\n## Usage example\n\nPlugin provides `api` fixture, but you should define `aiohttp_app` fixture first:\n\n```python\nimport pytest\n\nfrom my_awesome_app import make_app\n\n\n@pytest.fixture\ndef aiohttp_app() -> Application:\n  return make_app()\n```\n\n### Default decoding\n\nFixture will decode and return payload by default as json or bytes (depends on `Content-Type` header):\n\n```python\nasync def test_returns_json(api):\n    got = await api.get("/json-url/")\n\n    assert got == {"key": "value"}\n\n\nasync def test_returns_bytes(api):\n    got = await api.get("/url/")\n\n    assert got == b"Some text"\n```\n\n### Status code assertions\n\nYou can assert on status code:\n\n```python\nasync def test_returns_ok(api):\n    await api.get("/url/", expected_status=200)\n```\n\n### `Response` result\n\nType `as_response=True` if you need `ClientResponse` object:\n\n```python\nfrom aiohttp.client import ClientResponse\n\nasync def test_returns_response(api):\n    got = await api.get("/url/", as_response=True)\n\n    assert isinstance(got, ClientResponse)\n```\n\n## Development and contribution\n\nFirst of all you should install [Poetry](https://python-poetry.org).\n\n- install project dependencies\n\n```bash\nmake install\n```\n\n- run linters\n\n```bash\nmake lint\n```\n\n- run tests\n\n```bash\nmake test\n```\n\n- feel free to contribute!\n',
    'author': 'Nikita Sivakov',
    'author_email': 'sivakov512@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sivakov512/pytest-aiohttp-client',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
