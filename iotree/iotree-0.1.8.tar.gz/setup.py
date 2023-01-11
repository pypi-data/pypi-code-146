# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iotree',
 'iotree.cli',
 'iotree.core',
 'iotree.core.io',
 'iotree.core.render',
 'iotree.utils']

package_data = \
{'': ['*'], 'iotree': ['config/*', 'examples/*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'orjson>=3.8.5,<4.0.0',
 'pytest>=7.2.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=10.11.0,<13.0.0',
 'soup2dict>=2.1.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.7.0,<0.8.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['iotree = iotree.__main__:app']}

setup_kwargs = {
    'name': 'iotree',
    'version': '0.1.8',
    'description': 'A lightweight CLI + lib that allows you to perform basic IO tasks and display your content as rich trees and tables.',
    'long_description': '# A many-in-one tool for managing your Markup Language files.\n\n## What is it?\n\n**iotree** is a tool for managing your Markup Language files. It is capable to write and read files in the following formats:\n\n- JSON\n- YAML\n- TOML\n- XML\n- And soon more... :wink:\n\nThe basic goal was to have a small package anyone could add to their project and use it to manage their files. It is also possible to use it as a CLI tool.\n\n## Installation\n\nYou cannot install the CLI tool separately for now. You can install it with the following command:\n\n```bash\npip install iotree\n```\n\n## Usage\n\n### As a CLI tool\n\nTo see what the display function can do, you can use the following command:\n\n```bash\niotree demo\n```\n\nFor example, the following JSON file (displayed in VSCode)\n\n```json\n{\n    "glossary": {\n        "title": "example glossary",\n        "GlossDiv": {\n            "title": "S",\n            "GlossList": {\n                "GlossEntry": {\n                    "ID": "SGML",\n                    "SortAs": "SGML",\n                    "GlossTerm": "Standard Generalized Markup Language",\n                    "Acronym": "SGML",\n                    "Abbrev": "ISO 8879:1986",\n                    "GlossDef": {\n                        "para": "A meta-markup language, used to create markup languages such as DocBook.",\n                        "GlossSeeAlso": [\n                            "GML",\n                            "XML"\n                        ]\n                    },\n                    "GlossSee": "markup"\n                }\n            }\n        }\n    }\n}\n```\n\nwill be displayed like this:\n\n![JSON file displayed](https://i.imgur.com/tUSyW3L.png)\n\nWhile the following YAML file (displayed in VSCode)\n\n```yaml\t\n---\n doe: "a deer, a female deer"\n ray: "a drop of golden sun"\n pi: 3.14159\n xmas: true\n french-hens: 3\n calling-birds:\n   - huey\n   - dewey\n   - louie\n   - fred\n xmas-fifth-day:\n   calling-birds: four\n   french-hens: 3\n   golden-rings: 5\n   partridges:\n     count: 1\n     location: "a pear tree"\n   turtle-doves: two\n```\n\nwill be displayed like this:\n\n![YAML file displayed](https://i.imgur.com/t3q5yHS.png)\n\n**Note**: The CLI tool is not yet finished. It is still in development.  \nIf this just looks like a wrapper around [rich trees](https://rich.readthedocs.io/en/stable/tree.html)) to you, it almost because it is. :wink:\n\nAs a CLI tool, the key difference I want to bring is the ability to configure *themes* and *styles*.\n\nJust run the following command to interactively create a theme:\n\n```bash\niotree config init\n```\n\nBut if you\'re lazy, just use a file:\n\n```bash\niotree config init from-json my_theme.json\n```\n\nFor example, the following JSON file\n\n```json\n{   \n    "name": "My super pseudonym",\n    "username": "my.username",\n    "symbol": "lgpoint",\n    "theme": "bright-blue-green"\n}\n```\n\nwill result in the following theme: ... ',
    'author': 'Arno V',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
