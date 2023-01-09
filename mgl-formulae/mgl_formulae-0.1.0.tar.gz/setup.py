# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mgl_formulae']

package_data = \
{'': ['*']}

install_requires = \
['lark>=1.1.4,<2.0.0']

setup_kwargs = {
    'name': 'mgl-formulae',
    'version': '0.1.0',
    'description': 'Conversion to/from a human-oriented formula representation for mapbox-gl expression language',
    'long_description': '# Formula syntax for Mapbox GL expressions\n\nA library for converting [Mapbox GL expressions](https://www.mapbox.com/mapbox-gl-js/style-spec/#expressions) to/from\na formula syntax more familiar to humans (extended JavaScript-like grammar).\n\n## Syntax examples\n\n```js\n// Expression\n["+", 3, 4]\n// Formula\n3 + 4\n```\n\n```js\n// Expression\n["==", ["coalesce", ["get", "foo"], -1], 1]\n// Formula\n(get("foo") ?? -1) == 1\n```\n\n```js\n// Expression\n["min", ["zoom"], ["log2", 3.14]]\n// Formula\nmin(zoom(), log2(3.14))\n```\n\n```js\n// Expression\n[\n    "!=",\n    ["+", ["*", 3, 4], ["get", "foo"]],\n    ["-", 4, ["/", 3, 2]]\n]\n// Formula\n3 * 4 + get("foo") != 4 - 3 / 2\n```\n\n```js\n// Expression\n["concat", "id: ", ["number-format", ["get", "id"], {}]]\n// Formula\n"label: " & number_format(get("id"), {})\n```\n\n## Usage\n\n```python\nfrom mgl_formulae import FormulaCompiler, FormulaDecompiler\ncompiler = FormulaCompiler.create()\ndecompiler = FormulaDecompiler.create()\n\nassert compiler.compile(\'3 + 4\') == [\'+\', 3, 4]\nassert decompiler.decompile([\'+\', 3, 4]) == \'3 + 4\'\n```\n\n## Features\n* Transparent function calls: any unknown expression turns into a function call automatically, \n  simplifying forward compatibility when new language functions are added\n* Automatic conversion between dash in expressions and underscore in function names:\n  e.g. `number-format` and `number_format`\n* Rich infix operator set for common operations with JavaScript precedence/associativity\n* Automatic conversion between if/else chains, ternary conditionals and `case` expressions \n* Full support for all json literal values, including `literal` conversion for lists and objects\n* Support for functions with keyword arguments (e.g. `format`)\n* Syntactic sugar for `let`/`var`: `let $foo = 42; 1 + $foo`\n\n## Non-trivial operator table\n\n|   Operator   | Expression |\n|:------------:|:----------:|\n|      ??      |  coalesce  |\n| &#124;&#124; |    any     |\n|      &&      |    all     |\n|      &       |   concat   |\n|  a ? b : c   |   case/3   |\n\nOther common operators are preserved as-is, while having the expected JavaScript-like semantics. \n',
    'author': 'Nikita Ofitserov',
    'author_email': 'himikof@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/himikof/mgl-formulae',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
