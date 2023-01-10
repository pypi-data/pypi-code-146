# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['col_spanish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'col-spanish',
    'version': '0.0.4',
    'description': 'Functions that help to work with text in spanish (Colombia)',
    'long_description': '# col-spanish\nA collection of tools to work with text write in Spanish (Colombia)\n\n\n### Purpose of the Package\nThe purpose of the package is to create a group of functions that help to work with text in spanish, to be more accurate with spanish from Colombia.\n\n### Features\n+ normalization functions:\n    - delete punctuation marks\n    - delete accents\n\n+ encrypting functions:\n    - set_characters: \n        > delete duplicate characters inside the sentence. save it in the same order, \n        > as it appears in the sentence not in an aleatory order as set()\n    - create_dictionary: \n        > Recieves two lists and create a dictionary where one is the key and the\n        > other one is the value.\n    - generate_pass: \n        > This function create a safe encrypted version of your data.\n\n### Geting Started\nThe package can be found in Pypi, hence you can install it using pip\n```bash\npip install col_spanish\n```\n\n### Usage\nUsing the normalization function to remove punctuation marks\n```python\n>>> from col_spanish import del_punctuation\n>>> del_punctuation(\'Hola, ¿cómo estas? ¡bien!\')\n>>>\n```\n\n### Examples\n```python\n>>> from col_spanish import del_punctuation\n\n>>> del_punctuation(\'Hola, ¿cómo estas? ¡bien!\')\nHola cómo estas bien\n\n>>> text = "Hola, ¿cómo estas? ¡bien!"\n>>> normalized_text = del_punctuation(text)\n>>> normalized_text\nHola cómo estas bien\n```\n\n### Contribution\nContributions are welcolme.\nIf you notice a bug let us know, thanks!\n\n### Author\n+ Main maintainer: Sergio A. Sosa Bautista (@sergioasb8)',
    'author': 'Sergio Sosa Bautista',
    'author_email': 'sergioasb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sergioasb8/col-spanish',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
