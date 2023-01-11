# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helios_ls']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'pygls==0.13.1', 'tree-sitter>=0.20.1,<0.21.0']

entry_points = \
{'console_scripts': ['helios-language-server = helios_ls.server:main']}

setup_kwargs = {
    'name': 'helios-language-server',
    'version': '0.2.0',
    'description': 'Language server for Helios, a non-Haskell Cardano smart contract DSL.',
    'long_description': '# helios-language-server\n\n[![image-version](https://img.shields.io/pypi/v/helios-language-server.svg)](https://python.org/pypi/helios-language-server)\n[![image-python-versions](https://img.shields.io/badge/python=3.10-blue)](https://python.org/pypi/helios-language-server)\n\nLanguage server for <a href="https://github.com/Hyperion-BT/Helios">Helios</a>, a non-Haskell Cardano smart contract language.\nUses the <a href="https://github.com/openlawlibrary/pygls">pygls</a> lsp framework and <a href="https://github.com/tree-sitter/tree-sitter">tree-sitter</a> for syntax tree generation.\n\n![auto-complete](./img/auto-complete.gif)\n\n## Requirements\n\n* `Python 3.10`\n* `python3-pip` (Ubuntu/Debian)\n* `python3-venv` (Ubuntu/Debian)\n\n## Installation\n\n### coc.nvim\n1. Easy way via npm package <a href="https://github.com/et9797/coc-helios">coc-helios</a>:\n\n    `:CocInstall coc-helios`\n\n2. Alternatively, if you know how to set up Python virtual environments:\n\n    `python3 -m venv .venv` <br>\n    `source .venv/bin/activate` <br>\n    `pip install helios-language-server`\n    \n    Put this in your `coc-settings.json` file (`:CocConfig`):\n    \n    ```json\n    {\n        "languageserver": {\n          "helios": {\n            "command": "helios-language-server",\n            "args": ["--stdio"],\n            "filetypes": ["*.hl", "hl"]\n        }\n    }\n    ```\n    The language server should now activate whenever you open `.hl` files, provided you have `filetype.nvim` plugin installed. \n\n### VSCode\n\n&emsp; See <a href="https://github.com/Et9797/vscode-helios">vscode-helios</a>.\n\n## Capabilities\n- [x] Auto-completions\n- [x] Hover\n- [x] Signature help\n- [ ] Syntax errors\n- [ ] Go to definition\n\n## Comments and tips (**IMPORTANT**)\nCurrently only supports builtin types and methods up until **Helios v0.9.2** (apart from import statements).\n\nWhile in general the tree-sitter parser works okay, there are several shortcomings as it is not always error tolerant. \nMeaning that if there are syntax errors present in the source code, the parser can sometimes generate error nodes spanning the entire document. \nThis may lead to no/unexpected auto-completions. Unfortunately, not too much can be done about the parser\'s error recovery ability at this stage, \nas this is still also an open <a href="https://github.com/tree-sitter/tree-sitter/issues/1870#issuecomment-1248659929">issue</a> with tree-sitter. \nI have tried to address some commonly occuring parsing errors.\n\n## To-dos\n- Parser improvements\n- Advanced diagnostics\n- Semantic highlighting\n- Imports\n- Go to definition\n- Support newer Helios versions\n- Tree-sitter syntax highlighting (nvim)\n- Type checking\n',
    'author': 'et',
    'author_email': 'etet1997@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
