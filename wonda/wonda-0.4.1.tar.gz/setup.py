# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wonda',
 'wonda.api',
 'wonda.api.request_validator',
 'wonda.api.response_validator',
 'wonda.api.utils',
 'wonda.bot',
 'wonda.bot.blueprint',
 'wonda.bot.dispatch',
 'wonda.bot.dispatch.handlers',
 'wonda.bot.dispatch.labelers',
 'wonda.bot.dispatch.middlewares',
 'wonda.bot.dispatch.return_manager',
 'wonda.bot.dispatch.router',
 'wonda.bot.dispatch.view',
 'wonda.bot.polling',
 'wonda.bot.rules',
 'wonda.bot.states',
 'wonda.bot.states.dispenser',
 'wonda.bot.updates',
 'wonda.contrib',
 'wonda.contrib.rules',
 'wonda.contrib.storage',
 'wonda.errors',
 'wonda.errors.error_handler',
 'wonda.errors.swear_handler',
 'wonda.http',
 'wonda.tools',
 'wonda.tools.keyboard',
 'wonda.tools.storage',
 'wonda.tools.text',
 'wonda.tools.text.formatting',
 'wonda.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'certifi>=2022.6.15,<2023.0.0',
 'choicelib>=0.1.5,<0.2.0',
 'pydantic>=1.9.0,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0',
 'vbml>=1.1.post1,<2.0']

extras_require = \
{'auto-reload': ['watchfiles>=0.16.0,<0.17.0'],
 'power-ups': ['orjson>=3.7.11,<4.0.0', 'uvloop>=0.16.0,<0.17.0']}

setup_kwargs = {
    'name': 'wonda',
    'version': '0.4.1',
    'description': 'Asynchronous, feature-rich, high performant Telegram Bot API framework for building stunning bots',
    'long_description': '# Wonda ✨\n\n[//]: # (Examples)\n[examples]: examples/high_level\n[text formatting]: examples/high_level/formatting_example.py\n[middleware]: examples/high_level/setup_middleware.py\n[file uploading]: examples/high_level/file_upload_example.py\n[blueprints]: examples/high_level/load_blueprints.py\n[FSM]: examples/high_level/use_state_dispenser.py\n\n[//]: # (Badges)\n![Version](https://img.shields.io/pypi/v/wonda?label=version&style=flat-square)\n![Package downloads](https://img.shields.io/pypi/dw/wonda?label=downloads&style=flat-square)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/wonda?label=supported%20python%20versions&style=flat-square)\n\n## Why\n\nWonda can help you build bots using simple tools without losing performance. It has all batteries included: [text formatting], [file uploading], [blueprints], [middleware] and [FSM] are usable right away.\n\n## Versions\n\n### Stable or pre-release\n\nTo install a stable version of Wonda, enter this command in your terminal:\n\n```shell script\npip install -U wonda\n```\n\nIf you decide to go beta, use the same command with `--pre` option or update from dev branch .zip [archive](https://github.com/wondergram-org/wonda/archive/refs/heads/dev.zip).\n\n### Performance\n\nYou can make Wonda perform even better by installing power-ups. They\'re optional, but highly recommended.\n\n```shell script\npip install --force wonda[power-ups]\n```\n\nTo see the full list of packages, refer to our [project file](pyproject.toml).\n\n## Guide\n\nIt\'s easy to build a bot with Wonda — it\'s ready in *six* lines of code. Extending it is no problem too.\n\n```python\nfrom wonda import Bot\n\nbot = Bot("your-token")\n\n\n@bot.on.message()\nasync def handler(_) -> str:\n    return "Hello world!"\n\nbot.run_forever()\n```\n\nWith Wonda, it\'s possible to achieve this much with so little code. To get started, check out our [examples].\n\n## Contributing\n\nWonda is a work in progress and a lot of stuff is expected to change! It\'s the right time for your input.\n\nIf you want to report a bug or suggest a feature, [create an issue](https://github.com/wondergram-org/wonda/issues/new/choose). To ask a question, please use [discussions](https://github.com/wondergram-org/wonda/discussions). Big thanks!\n\n## License\n\nThis project is MIT licensed. Based upon hard work of maintainers and contributors of [VKBottle](https://github.com/vkbottle/vkbottle).\n\nCopyright © timoniq (2019-2021), feeeek (2022), geo-madness (2022)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/wonda/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
