# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncpg_engine']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.27.0,<0.28.0']

entry_points = \
{'pytest11': ['asyncpg_engine = asyncpg_engine.pytest_plugin']}

setup_kwargs = {
    'name': 'asyncpg-engine',
    'version': '0.3.1',
    'description': 'Wrapper around asyncpg with a bit better experience.',
    'long_description': '# asyncpg-engine\n\nSmall wrapper around [asyncpg](https://github.com/MagicStack/asyncpg) for specific experience and transactional testing.\n\n[![test Status](https://github.com/sivakov512/asyncpg-engine/actions/workflows/test.yml/badge.svg)](https://github.com/sivakov512/asyncpg-engine/actions/workflows/test.yml)\n[![Coverage Status](https://coveralls.io/repos/github/sivakov512/asyncpg-engine/badge.svg?branch=master)](https://coveralls.io/github/sivakov512/asyncpg-engine?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Python versions](https://img.shields.io/pypi/pyversions/asyncpg-engine.svg)](https://pypi.python.org/pypi/asyncpg-engine)\n[![PyPi](https://img.shields.io/pypi/v/asyncpg-engine.svg)](https://pypi.python.org/pypi/asyncpg-engine)\n\n## Basic usage\n\n```python\nfrom asyncpg_engine import Engine\n\n\nengine = await Engine.create("postgres://guest:guest@localhost:5432/guest?sslmode=disable")\n\nasync with engine.acquire() as con:\n    # https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.Connection\n    assert await con.fetchval("SELECT 1") == 1\n```\n\n### Custom type conversions\n\nYou can specify [custom encoder/decoder](https://magicstack.github.io/asyncpg/current/usage.html#custom-type-conversions) by subclassing `Engine`:\n```python\nfrom asyncpg_engine import Engine\nimport orjson\n\n\nclass MyEngine(Engine):\n\n    @staticmethod\n    async def _set_codecs(con: Connection) -> None:\n        # https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.Connection.set_type_codec\n        await con.set_type_codec(\n            "json", encoder=orjson.dumps, decoder=orjson.loads, schema="pg_catalog"\n        )\n```\n\n## Pytest plugin\n\nLibrary includes pytest plugin with support for transactional testing.\n\nTo start using it install `pytest`, enable plugin in your root `conftest.py` and define `postgres_url` fixture that returns database connection string:\n```python\npytest_plugins = ["asyncpg_engine"]\n\n\n@pytest.fixture()\ndef postgres_url() -> str:\n    return "postgres://guest:guest@localhost:5432/guest?sslmode=disable"\n```\n\nNow you can use two fixtures:\n\n* `db` that returns `Engine` instance:\n```python\nasync def test_returns_true(db):\n    async with db.acquire() as con:\n        assert await con.fetchval("SELECT true")\n```\n\n* `con` that returns already acquired connection:\n```python\nasync def test_returns_true(con):\n    assert await con.fetchval("SELECT true")\n```\n\nBy default `Engine` is configured for transactional testing, so every call to `db.acquire` or `con` usage will return the same connection with already started transaction. Transaction is rolled back at the end of test, so all your changes in db are rolled back too.\n\nYou can override this behaviour with `asyncpg_engine` mark:\n```python\n@pytest.mark.asyncpg_engine(transactional=False)\nasync def test_returns_true(con):\n    assert await con.fetchval("SELECT true")\n\n\n@pytest.mark.asyncpg_engine(transactional=False)\nasync def test_returns_true_too(db):\n    async with db.acquire() as con:\n        assert await con.fetchval("SELECT true")\n```\n\nIf you want to use your own custom `Engine` subclass in tests you can define `asyncpg_engine_cls` fixture that returns it:\n```python\nfrom asyncpg_engine import Engine\n\n\nclass MyPrettyEngine(Engine):\n    pass\n\n\n@pytest.fixture()\ndef asyncpg_engine_cls() -> typing.Type[MyPrettyEngine]:\n    return MyPrettyEngine\n\n\nasync def test_returns_my_pretty_engine(db: MyPrettyEngine) -> None:\n    assert isinstance(db, MyPrettyEngine)\n```\n\n## Development and contribution\n\nFirst of all you should install [Poetry](https://python-poetry.org).\n\n* install project dependencies\n```bash\nmake install\n```\n\n* run linters\n```bash\nmake lint\n```\n\n* run tests\n```bash\nmake test\n```\n\n* feel free to contribute!\n',
    'author': 'Nikita Sivakov',
    'author_email': 'sivakov512@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sivakov512/asyncpg-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
