# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bolt_expressions', 'bolt_expressions.contrib']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.55.0', 'bolt>=0.17.7', 'mecha>=0.59.2', 'nbtlib==1.12.1']

setup_kwargs = {
    'name': 'bolt-expressions',
    'version': '0.12.2',
    'description': 'Provides pandas-like expressions capabilities to the bolt extension of mecha',
    'long_description': '# bolt-expressions\n\n[![GitHub Actions](https://github.com/rx-modules/bolt-expressions/workflows/CI/badge.svg)](https://github.com/rx-modules/bolt-expressions/actions)\n[![PyPI](https://img.shields.io/pypi/v/bolt-expressions.svg)](https://pypi.org/project/bolt-expressions/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bolt-expressions.svg)](https://pypi.org/project/bolt-expressions/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Discord](https://img.shields.io/discord/900530660677156924?color=7289DA&label=discord&logo=discord&logoColor=fff)](https://discord.gg/98MdSGMm8j)\n\n> a `pandas`-esque API for creating expressions within bolt\n\n## Introduction\n\nBolt is a scripting language which mixes both python and mcfunction. This package amplifies this language by adding an API for creating fluent expressions loosely based off of the `pandas` syntax. These expressions are use for simplifying large bits of scoreboard and storage operation allowing you to swiftly create complex operations with the ease of normal programming.\n\n```py\nfrom bolt_expressions import Scoreboard, Data\n\nmath = Scoreboard.objective("math")\nstorage = Data.storage(example:temp)\n\nstack = storage.hotbar[0]\n\nmath["@s"] = stack.Count * math["$cost"] + math["$value"] - stack.tag.discount * 0.75\n```\n->\n```mcfunction\nexecute store result score @s math run data get storage example:temp hotbar[0].Count 1\nscoreboard players operation @s math *= $cost math\nscoreboard players operation @s math += $value math\nexecute store result score $i1 bolt.expr.temp run data get storage example:temp hotbar[0].tag.discount 0.75\nscoreboard players operation @s math -= $i1 bolt.expr.temp\n```\n\n## Installation\n\nThe package can be installed with `pip`. Note, you must have `beet`, `mecha` and `bolt` installed to use this package.\n\n```bash\n$ pip install bolt-expressions\n```\n\n## Getting started\n\nThis package is designed to be used within any `bolt` script (either a `.mcfunction` or `bolt` file) inside a `bolt` enabled project. \n\n```yaml\nrequire:\n    - bolt\n    - bolt_expressions\n\npipeline:\n    - mecha\n```\n\nOnce you\'ve required `bolt` and `bolt_expressions`, you are able to import the python package directly inside your bolt script.\n\n```py\nfrom bolt_expressions import Scoreboard, Data\n```\nNow you\'re free to use the API objects. Create objectives, block, storage and entity nbt sources to easily write expressions as simple or complex as you like to make it.\n\n```py\nmath = Scoreboard.objective("math")\nexecutor = Data.entity("@s")\nblock = Data.block("~ ~ ~")\nstorage = Data.storage(example:storage)\n\nmath["$value"] = math["$points"] + executor.Health*10 + block.Items[0].Count - storage.discount\n\nstorage.values.append(math["$value"])\n```\n->\n```mcfunction\nexecute store result score $value math run data get entity @s Health 10\nscoreboard players operation $value math += $points math\nexecute store result score $i1 bolt.expr.temp run data get block ~ ~ ~ Items[0].Count 1\nscoreboard players operation $value math += $i1 bolt.expr.temp\nexecute store result score $i2 bolt.expr.temp run data get storage example:storage discount 1\nscoreboard players operation $value math -= $i2 bolt.expr.temp\ndata modify storage example:storage values append value 0\nexecute store result storage example:storage values[-1] int 1 run scoreboard players get $value math\n```\n\n## Features\n\n- Robust API supporting Scoreboards, Storage, Blocks, and Entities\n- Provides an interface to manipulate large, complex mathematical expressions simplily\n- Automatically initializes objectives and score constants\n- Allows you to interopt custom variables with normal commands\n\nCheckout some examples over at our [docs](https://rx-modules.github.io/bolt-expressions/)!\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort bolt_expressions examples tests\n$ poetry run black bolt_expressions examples tests\n$ poetry run black --check bolt_expressions examples tests\n```\n\n---\n\nLicense - [MIT](https://github.com/rx-modules/bolt-expressions/blob/main/LICENSE)\n',
    'author': 'rx97',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rx-modules/bolt-expressions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
