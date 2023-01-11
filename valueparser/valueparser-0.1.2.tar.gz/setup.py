# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valueparser']

package_data = \
{'': ['*']}

install_requires = \
['systemy>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'valueparser',
    'version': '0.1.2',
    'description': 'Python package for quick creation of tools to parse a value',
    'long_description': 'Parser\n======\n\nPython package for quick creation/ combination of value parser object for muly-puposes\n\nInstall\n=======\n\n```shell\n> pip install valueparser\n```\n\nUsage\n=====\n\n```python\nfrom valueparser.parsers import Bounded\n\nvalue_parser = Bounded(min=0, max=1)\n\nvalue_parser.parse(4.0)\n\n# ParseError: 4.0 is higher than 1.0\n```\n\nSeveral parsers can be combined to one single parser object, they share however the same name space for configuration\nparameters\n\n```python \nfrom valueparser import parser, Clipped, Rounded\n\nratio_parser = parser( (float, Clipped, Rounded),  min=0, max=1.0, ndigits=2 )\n\nassert ratio_parser.parse( 0.231234) == 0.23 \nassert ratio_parser.parse( 4.5) == 1.0 \nassert ratio_parser.parse( "0.12345") == 0.12\n\n```\n\nEquivalent can be done by creating a new class \n\n```python \nfrom valueparser import parser_class, Clipped, Rounded\n\nMyParser = parser_class( (float, Clipped, Rounded), "MyParser" )\nratio_parser = MyParser( min=0, max=1, ndigits=2)\n```\n\n\n`conparser` works the same way than `parser` except it construct a typing object to be use inside pydantic BaseModel in\na compact way.\n\n\n```python \nfrom valueparser import conparser, Bounded\nfrom pydantic import BaseModel \n\nPixel =  conparser( (int, Bounded), min=0, max=1023 ) \nclass Data(BaseModel):\n    x: Pixel = 512\n    y: Pixel = 512\n   \nData(x=-200)\n\n# \n#pydantic.error_wrappers.ValidationError: 1 validation error for Data\n#x\n#    -200.0 is lower than 0.0 (type=value_error.parse; error_code=Errors.OUT_OF_BOUND)\n```\n\nto make any function a `parser` (e.g. an object with `parse` method) one can use the  `parser` function as well :\n\n```python\nfrom valueparser import parser\n\nfloat_parser = parser(float)\nassert float_parser.parse("1.234") == 1.234\n\nforce_int_parser = parser( (float, int)) # parse to float then int \nassert force_int_parser.parse( "1.234") == 1\n```\n\nActually the `parser` function accepts :\n\n- A Parser Class iddentified as a class with the `parse` method \n- A callable \n- An instance of a Parser Class\n- an mix inside an iterable \n\nPlus any kwargs accepted by the combination of parsers\n\nBuiltin Parsers \n===============\n\n| class name |  kwargs | comment | \n|------------|---------|---------|\n| Bounded    | min=-inf, max=+inf | raise an error if value outside interval else return value |\n| Clipped    | min=-inf, max=+inf | clip silently the value to inferior and superior bounds | \n| Rounded    | ndigits=0          | round the numerical value to ndigits           |\n| Formated   | format="%s"        | convert to string with the given format        |\n| Listed     | items=[], default_item(optional) |  raise error if value not in items list else return value a\n|            |                                  | default_item can be set to be returned instead of error raised |\n| Enumerated  | enumerator                        | return enumerator(value) or raise error | \n\n\nCreate a custom parser\n======================\n\nTo create a parser one need to create a new class from BaseParser, declare any configurable argument \ninside the child class ``Config``  and define the static or classmethod `__parse__`\n\nFor instance a parser adding some noise to a value ( can be usefull for e.i. a simulator) \n\n```python\nfrom valueparser import BaseParser\nimport random \n\nclass Noisier(BaseParser):\n    class Config:\n        noise_scale = 1.0\n    @staticmethod\n    def __parse__( value, config):\n        return value + (random.random()-0.5) * config.noise_scale\n```\n\nUsage : \n\n```python\nnoisier = Noisier( noise_scale=100)\nx = noisier.parse(0.0)\nx\n36.700125482238036\n```\n\nOr use conparser in pydantic Model: \n\n```python \nfrom valueparser import conparser \nfrom pydantic import BaseModel  \n\nclass MyData(BaseModel):\n    x: conparser(Noisier, noise_scale=100)\n    y: conparser(Noisier, noise_scale=100)\n\nmy_data = MyData(x=0, y=0)\nmy_data\nMyData(x=32.819723479459284, y=-25.95893228872207)\n```\n\n\nParser and Systemy \n==================\n\nParsers are beased on :class:`systemy.System` class. One can include a parser factory in \na systemy class and expose the parser configuration to user. \n\n```python \nfrom valueparser import ParserFactory , Bounded\nfrom systemy import BaseSystem \nfrom pydantic import AnyUrl \n\ndummy = lambda x:x \n\nclass Node(BaseSystem):\n    class Config:\n        url: AnyUrl = "http://localhost:4840"\n        parser: ParserFactory = ParserFactory(type=dummy)\n\n    def set(self, value):\n        value = self.parser.parse(value) \n        # set value on server \n        return value\n\nnode = Node( parser={\'type\':(float,Bounded), \'min\':0, \'max\':10} )\n```\n\n\n\n\n\n\n\n',
    'author': 'Sylvain Guieu',
    'author_email': 'sylvain.guieu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
