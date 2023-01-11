# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokelance',
 'pokelance.cache',
 'pokelance.ext',
 'pokelance.http',
 'pokelance.models',
 'pokelance.models.abstract',
 'pokelance.models.abstract.utils',
 'pokelance.models.common']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'attrs>=22.1.0,<23.0.0',
 'types-aiofiles>=22.1.0.4,<23.0.0.0']

setup_kwargs = {
    'name': 'pokelance',
    'version': '0.0.5a0',
    'description': 'A flexible and easy to use pokemon library.',
    'long_description': '<h1 align="center"><b>PokeLance</b></h1>\n<p align="center">\n<img src="https://raw.githubusercontent.com/FallenDeity/PokeLance/master/docs/assets/pokelance.png" width=450 alt="logo"><br><br>\n<img src="https://img.shields.io/github/license/FallenDeity/PokeLance?style=flat-square" alt="license">\n<img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n<img src="https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat-square" alt="mypy">\n<img src="https://img.shields.io/badge/%20linter-ruff-%231674b1?style=flat-square" alt="ruff">\n<img src="https://img.shields.io/github/stars/FallenDeity/PokeLance?style=flat-square" alt="stars">\n<img src="https://img.shields.io/github/last-commit/FallenDeity/PokeLance?style=flat-square" alt="commits">\n<img src="https://img.shields.io/pypi/pyversions/PokeLance?style=flat-square" alt="py">\n<img src="https://img.shields.io/pypi/v/PokeLance?style=flat-square" alt="versions">\n<br><br>\nA flexible, statically typed and easy to use pokeapi wrapper for python 🚀\n</p>\n\n---\n\n\nFeatures:\n- Modern and pythonic API asynchronously built on top of aiohttp\n- Flexible and easy to use\n- Statically typed with mypy\n- Linted with ruff\n- Well documented\n- Optimized for speed and performance\n- Automatically caches data for faster access\n- Caches endpoints for user convenience\n\n---\n\n## Installation\n\n```bash\n$ python -m pip install PokeLance\n```\n\n---\n\n## Usage\n\n```python\nimport asyncio\n\nfrom pokelance import PokeLance\n\nclient = PokeLance()  # Create a client instance\n\n\nasync def main() -> None:\n    print(await client.ping())  # Ping the pokeapi\n    print(await client.berry.fetch_berry("cheri"))  # Fetch a berry from the pokeapi\n    print(await client.berry.fetch_berry_flavor("spicy"))\n    print(await client.berry.fetch_berry_firmness("very-soft"))\n    print(client.berry.get_berry("cheri"))  # Get a cached berry it will return None if it doesn\'t exist\n    print(client.berry.get_berry_flavor("spicy"))\n    print(client.berry.get_berry_firmness("very-soft"))\n    await client.close()  # Close the client\n    return None\n\n\nasyncio.run(main())\n```\n\n## With Async Context Manager\n\n```python\nimport asyncio\n\nimport aiohttp\nfrom pokelance import PokeLance\n\n\nasync def main() -> None:\n    # Use an async context manager to create a client instance\n    async with aiohttp.ClientSession() as session, PokeLance(session=session) as client:\n        print(await client.ping())  # Ping the pokeapi\n        print(await client.berry.fetch_berry("cheri"))  # Fetch a berry from the pokeapi\n        print(await client.berry.fetch_berry_flavor("spicy"))\n        print(await client.berry.fetch_berry_firmness("very-soft"))\n        print(client.berry.get_berry("cheri"))  # Get a cached berry it will return None if it doesn\'t exist\n        print(client.berry.get_berry_flavor("spicy"))\n        print(client.berry.get_berry_firmness("very-soft"))\n        # The client will be closed automatically when the async context manager exits\n    return None\n\nasyncio.run(main())\n```\n\n## Important Links\n\n\n- [PokeAPI](https://pokeapi.co/)\n- [PokeAPI Documentation](https://pokeapi.co/docs/v2)\n- [PokeLance Documentation](https://FallenDeity.github.io/PokeLance/)\n- [PokeLance ReadTheDocs](https://pokelance.readthedocs.io/en/latest/)\n- [PokeLance GitHub](https://github.com/FallenDeity/PokeLance)\n- [PokeLance PyPI](https://pypi.org/project/PokeLance/)\n- [PokeLance Discord](https://discord.gg/yeyEvT5V2J)\n\n---\n\n!!! note "Note"\n    This is a work in progress. If you find any bugs or have any suggestions, please open an issue [here](https://github.com/FallenDeity/PokeLance/issues/new).\n\n---',
    'author': 'FallenDeity',
    'author_email': '61227305+FallenDeity@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
