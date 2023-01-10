# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telebot_components',
 'telebot_components.broadcast',
 'telebot_components.constants',
 'telebot_components.feedback',
 'telebot_components.form',
 'telebot_components.form.helpers',
 'telebot_components.menu',
 'telebot_components.redis_utils',
 'telebot_components.stores',
 'telebot_components.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'markdown>=3.4.1,<4.0.0',
 'markdownify>=0.11.2,<0.12.0',
 'py-trello>=0.18.0,<0.19.0',
 'pyairtable>=1.3.0,<2.0.0',
 'pytest-mock>=3.7.0,<4.0.0',
 'redis>=4.3.1,<5.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'telebot-against-war>=0.5.4,<0.6.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'telebot-components',
    'version': '0.6.0',
    'description': 'Framework/toolkit for building Telegram bots with telebot and redis',
    'long_description': "# telebot-components\n\nFramework / toolkit for building bots with [telebot](https://github.com/bots-against-war/telebot).\n\n<!-- ## Development -->\n\n## Development\n### Setup\n1. Clone repository\n   ```bash\n   git clone git@github.com:bots-against-war/telebot-components.git baw\n   cd ./baw\n   ```\n\n2. The project requires Poerty 1.2.x or higher (see [installation instruction](https://python-poetry.org/docs/master#installing-with-the-official-installer))).\n   For example, to install `1.2.0b2` on Unix, run\n   ```bash\n   curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0b2\n   ```\n\n3. Then, to install the library with all dependencies, run from project root\n   ```bash\n   poetry install\n   ```\n   - You might need to manually install dynamic versioning plugin (without it local build will\n     always have version `0.0.0`):\n     ```bash\n     poetry plugin add poetry-dynamic-versioning-plugin\n     ```\n   - To create virtualenv inside the project’s root directory, use command\n     ```bash\n     poetry config virtualenvs.in-project false --local\n     ```\n4. Run `pre-commit` to set up git hook scripts\n   ```bash\n   pre-commit install\n   ```\n\n\n### Testing\nUse command below for run tests\n```bash\npoetry run pytest tests -vv\n```\n\nBy default, all tests are run with in-memory Redis emulation. But if you want you can run them\nlocally on real Redis (**read manual below**) \n\n> **Note**: Tests must be able to find an empty Redis DB to use; they also clean up after themselves.\n\n### Start example bot\nFor first start you need to do 3 things:\n1. Use command below to generate environment variables file:\n    ```bash\n    cp ./examples/example.env ./examples/.env\n    ```\n   > **Note**: After `.env` file is generated you will need to add your [bot's token](https://core.telegram.org/bots#6-botfather) to it.  \n   > Also for bot with `trello integration` you need to add `trello` token and api key. You can get it [here](https://trello.com/app-key).\n2. If you want start redis on local machine, run\n    ```bash\n    docker run --name baw-redis -d -p 6379:6379 redis redis-server --save 60 1 --loglevel warning\n    ```\n3. Run any bot from `./examples`\n    ```bash\n    python3 ./examples/feedback_bot.py  // or run with IDE from bot file\n    ```\n",
    'author': 'Igor Vaiman',
    'author_email': 'gosha.vaiman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bots-against-war/telebot-components',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
