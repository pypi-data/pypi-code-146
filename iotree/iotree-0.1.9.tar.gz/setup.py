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
    'version': '0.1.9',
    'description': 'A lightweight CLI + lib that allows you to perform basic IO tasks and display your content as rich trees and tables.',
    'long_description': '# A many-in-one tool for managing your Markup Language files.\n\n## What is it?\n\n**iotree** is a tool for managing your Markup Language files. It is capable to write and read files in the following formats:\n\n- JSON\n- YAML\n- TOML\n- XML\n- And soon more... 😉\n\nThe basic goal was to have a small package anyone could add to their project and use it to manage their files. It is also possible to use it as a CLI tool.\n\n## Installation\n\nYou cannot install the CLI tool separately for now. You can install it with the following command:\n\n```bash\npip install iotree\n```\n\n## Usage\n\n### As a CLI tool\n\nTo see what the display function can do, you can use the following command:\n\n```bash\niotree demo\n```\n\nFor example, the following JSON file (displayed in VSCode)\n\n```json\n{\n    "glossary": {\n        "title": "example glossary",\n        "GlossDiv": {\n            "title": "S",\n            "GlossList": {\n                "GlossEntry": {\n                    "ID": "SGML",\n                    "SortAs": "SGML",\n                    "GlossTerm": "Standard Generalized Markup Language",\n                    "Acronym": "SGML",\n                    "Abbrev": "ISO 8879:1986",\n                    "GlossDef": {\n                        "para": "A meta-markup language, used to create markup languages such as DocBook.",\n                        "GlossSeeAlso": [\n                            "GML",\n                            "XML"\n                        ]\n                    },\n                    "GlossSee": "markup"\n                }\n            }\n        }\n    }\n}\n```\n\nwill be displayed like this:\n\n![JSON file displayed](https://i.imgur.com/tUSyW3L.png)\n\nWhile the following YAML file (displayed in VSCode)\n\n```yaml\t\n---\n doe: "a deer, a female deer"\n ray: "a drop of golden sun"\n pi: 3.14159\n xmas: true\n french-hens: 3\n calling-birds:\n   - huey\n   - dewey\n   - louie\n   - fred\n xmas-fifth-day:\n   calling-birds: four\n   french-hens: 3\n   golden-rings: 5\n   partridges:\n     count: 1\n     location: "a pear tree"\n   turtle-doves: two\n```\n\nwill be displayed like this:\n\n![YAML file displayed](https://i.imgur.com/t3q5yHS.png)\n\n**Note**: The CLI tool is not yet finished. It is still in development.  \nIf this just looks like a wrapper around [rich trees](https://rich.readthedocs.io/en/stable/tree.html)) to you, it almost because it is. :wink:\n\nAs a CLI tool, the key difference I want to bring is the ability to configure *themes* and *styles*.\n\nJust run the following command to interactively create a theme:\n\n```bash\niotree config init\n```\n\nBut if you\'re lazy, just use a file:\n\n```bash\niotree config init from-json my_theme.json\n```\n\nFor example, the following JSON file\n\n```json\n{   \n    "name": "My super pseudonym",\n    "username": "my.username",\n    "symbol": "lgpoint",\n    "theme": "bright-blue-green"\n}\n```\n\nDoes _not_ immediately affect the display of the files. You need to use the following command:  \nTo understand why, you can run\n\n```bash\niotree config ls # same as iotree cfg ls\n```\n\nThis is what the output looks like:\n\n![iotree config ls](https://i.imgur.com/5R3IMUG.png)\n\nYou can see that the theme is registered, but will **not** be used by default.\nThe best proof of this is to ask who the current user is:\n\n```bash\niotree cfg get last_user\n#> ✅ Config found for user arnov\n#> arnov\n```\nSo the current user is `arnov`. To use _YOUR_ theme, you need to run the following command:\n\n```bash\niotree cfg set last_user my.username\n#> 👷 Config: last_user ===> my.username\n```\n\nNow, if you try to render a file, you will see that the theme is used:\n\n```bash\niotree render .\\iotree\\examples\\example.toml\n```\n\nHere\'s what the output looks like:\n\n![iotree render after](https://i.imgur.com/RHROUWg.png)\n\nThe theme is now used. 🎉🎉\n\n### As a Python package\n\nYou can use the package in your Python project. Here\'s an example:\n\n```python\nfrom iotree.core.render import build\n\nmydict = {\n    "super" : {\n        "dict": {\n            "just": {\n                "for": {\n                    "example": "🤷\u200d♂️"\n                }\n            }\n        }\n    }\n}\n\n# Build the tree from the dict without hassle\n\ntree = build(mydict) # or build(mydict, theme="my_style", symbol="my_symbol")\n\n# Display the rich tree later\n\nconsole.print(tree) # or rich.print(tree)\n```\n\nBut there is more. You can also use the \'all in one\' IO from the package:\n\n```python\nfrom iotree.core.io import reader, writer\n\n# Read a file, any extension is supported from the list\n\ndict_one = reader.read("my_file.json")\ndict_two = reader.read("my_file.yaml")\ndict_three = reader.read("my_file.toml")\ndict_four = reader.read("my_file.xml")\ndict_five = reader.read("my_file.html")\n\n# ... do some manipulations, like possibly merging the dicts or creating a new one\n\n# Write the dict to a file\n\nwriter.write("my_file.json", dict_one)\nwriter.write("my_file.yaml", dict_two)\nwriter.write("my_file.toml", dict_three)\nwriter.write("my_file.xml", dict_four)\n# writer.write("my_file.html", dict_five) # Not supported yet\n```\n\nAnother small feature is the ability to _detect the type of a file_:\n\n```python\ndict_guess = reader.read("mysterious_file.not_a_real_extension")\n# if the content of the file is one of the supported types, it will be read correctly\n```\n\nThere\'s also a functional package, which is not yet documented.  \nIt allows you to compose functions while displaying rich progress using `rich.progress`.\n\n## Contributing\n\nIf you want to contribute, you can do so by forking the repository and creating a pull request.\n\nYou can also help me pick the new themes and symbols.\n\nTo see the possibilities, just run either of the following commands:\n\n```bash\niotree view themes # or\niotree view symbols # or\niotree view colors\n```',
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
