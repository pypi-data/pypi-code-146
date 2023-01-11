# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yada']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 't2-yada',
    'version': '1.2.0',
    'description': 'Yet another dataclass argparse',
    'long_description': '# Yada\n\n![PyPI](https://img.shields.io/pypi/v/t2-yada)\n![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)\n[![GitHub Issues](https://img.shields.io/github/issues/binh-vu/yada.svg)](https://github.com/binh-vu/yada/issues)\n![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nYada (**Y**et **A**nother **D**ataclass **A**rgument Parser!) is a library to automatically generate `argparse.ArgumentParser` given data classes. Compared to some available options such as: [Huggingface\'s HfArgumentParser](https://huggingface.co/transformers/v4.2.2/_modules/transformers/hf_argparser.html), [argparse_dataclass](https://github.com/mivade/argparse_dataclass), and [tap](https://github.com/swansonk14/typed-argument-parser), it offers the following benefits:\n\n1. Static Type Checking\n2. Nested data classes and complex types\n3. Easy to extend and customize the parser\n4. Generate command line arguments given the data classes.\n\n## Installation\n\nInstall via PyPI (requires Python 3.8+):\n\n```bash\npip install t2-yada\n```\n\n## How to use\n\nYada\'s parser can be constructed from data classes. It relies on fieds\' annotated types to construct correct argument parsers.\n\n```python\nimport yada\nfrom dataclasses import dataclass\nfrom typing import *\n\n@dataclass\nclass CityArgs:\n    city: Literal["LA", "NY"]\n\n\n@dataclass\nclass NestedArgs:\n    name: str\n    nested: CityArgs\n\nparser = yada.YadaParser(NestedArgs)\nargs = parser.parse_args()  # or use parser.parse_known_args() -- the two functions are similar to argparse.parse_args or argparse.parse_known_args\n```\n\nNote: YadaParser is annotated as a generic type: `YadaParser[C, R]` where C denotes the classes, and R denotes the instance of the classes created from the arguments. Therefore, in the above example, C is inferred as NestedArgs, but R is unknown, hence the type of `args` variable is unknown. To overcome this typing limitation, Yada provides several options for up to 10 data classes (`yada.Parser1`, `yada.Parser2`, ...). Below is two examples:\n\n```python\nparser = yada.Parser1(NestedArgs)\nargs = parser.parse_args()  # <-- args now has type NestedArgs\n```\n\n```python\nparser = yada.Parser2((NestedArgs, CityArgs))\nargs = parser.parse_args()  # <-- args now has type Tuple[NestedArgs, CityArgs]\n```\n\nNote: we recommend to use one of the specific parsers `yada.Parser<N>` instead of the generic `yada.YadaParser` if possible as they provide strong typing support.\n\n### Configuring Yada\n\n<details>\n<summary>Add help message</summary>\n\nYada reads the help message from the `key` property of `dataclasses.Field.metadata`\n\n```python\nimport yada\nfrom dataclasses import dataclass, field\nfrom typing import *\n\n@dataclass\nclass CityArgs:\n    city: Literal["LA", "NY"] = field(metadata={"help": "city\'s which you want to get the timezone"})\n\nparser = yada.Parser1(CityArgs)\n```\n\n</details>\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/binh-vu/yada',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
