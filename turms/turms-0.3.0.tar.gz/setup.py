# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turms',
 'turms.cli',
 'turms.parsers',
 'turms.plugins',
 'turms.processors',
 'turms.stylers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.0',
 'graphql-core>=3.2.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rich>=11.0.0,<12.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.9"': ['astunparse>=1.6.3,<2.0.0'],
 'black': ['black>=22.1.0,<23.0.0'],
 'isort': ['isort>=5.10.1,<6.0.0'],
 'watch': ['watchdog>=2.1.6,<3.0.0']}

entry_points = \
{'console_scripts': ['turms = turms.cli.main:entrypoint']}

setup_kwargs = {
    'name': 'turms',
    'version': '0.3.0',
    'description': 'graphql-codegen powered by pydantic',
    'long_description': '# turms\n\n[![codecov](https://codecov.io/gh/jhnnsrs/turms/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/turms)\n[![PyPI version](https://badge.fury.io/py/turms.svg)](https://pypi.org/project/turms/)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/turms/)\n![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/turms.svg)](https://pypi.python.org/pypi/turms/)\n[![PyPI status](https://img.shields.io/pypi/status/turms.svg)](https://pypi.python.org/pypi/turms/)\n[![PyPI download month](https://img.shields.io/pypi/dm/turms.svg)](https://pypi.python.org/pypi/turms/)\n\n## Goal\n\nTurms is a `graphql-codegen` inspired code generator for python that generates typed and serializable python code from your graphql schema and documents. Just define your query in standard graphql syntax and let turms create fully typed queries/mutation and subscriptions, that you can use in your favourite IDE.\n\nTurms allows you to easily generate both server-side and client-side code for your GraphQL API.\n\n### Schema (Server) Generation:\n\nCan generate the following types from your graphql SDL schema:\n\n- Enums\n- Inputs\n- Objects\n- Scalars\n- Directives\n\nSepcific generation supported for:\n\n- [x] Strawberry\n- [ ] Graphene\n\n### Documents (Client) Generation\n\nCan generate the following pydantic models from your graphql documents:\n\n- Enums\n- Inputs\n- Scalars\n- Fragments\n- Operations\n\n## Features\n\n- Fully typed, fully documented code generation\n- Schema and Document based code generation\n- Compatible with popular graphql libraries (strawberry, gql, rath, etc.)\n- Support for custom scalars, custom directives, ...\n- Powerful plugin system (e.g. custom Linting, custom formatting, etc.)\n- Operation functions like query, mutation, subscription (e.g. `data= get_capsules()`)\n- Compliant with graphl-config\n- Code migration support (trying to merge updates into existing code)\n\n## Installation\n\n```bash\npip install turms\n```\n\nturms is a pure development library and will not introduce any dependency on itself into your\ncode, so we recommend installing turms as a development dependency.\n\n```bash\npoetry add -D turms\n\n```\n\nAs of now turms only supports python 3.9 and higher (as we rely on ast unparsing)\n\n## Configuration\n\nTurms relies on and complies with [graphql-config](https://www.graphql-config.com/docs/user/user-introduction) and searches your current working dir for the graphql-config file.\n\n### Document based generation\n\nBased on pydantic models\n\n```yaml\nprojects:\n  default:\n    schema: http://api.spacex.land/graphql/\n    documents: graphql/**.graphql\n    extensions:\n      turms: # path for configuration for turms\n        out_dir: examples/api\n        plugins: # path for plugin configuration\n          - type: turms.plugins.enums.EnumsPlugin\n          - type: turms.plugins.inputs.InputsPlugin\n          - type: turms.plugins.fragments.FragmentsPlugin\n          - type: turms.plugins.operation.OperationsPlugin\n          - type: turms.plugins.funcs.FuncsPlugin\n        processors:\n          - type: turms.processor.black.BlackProcessor\n          - type: turms.processor.isort.IsortProcessor\n        scalar_definitions:\n          uuid: str\n          timestamptz: str\n          Date: str\n```\n\n### Schema based generation\n\nBased on strawberry models\n\n```yaml\nprojects:\n  default:\n    schema: beasts.graphql\n    extensions:\n      turms:\n        skip_forwards: true\n        out_dir: api\n        stylers:\n          - type: turms.stylers.capitalize.CapitalizeStyler\n          - type: turms.stylers.snake_case.SnakeCaseStyler\n        plugins:\n          - type: turms.plugins.strawberry.StrawberryPlugin # generates a strawberry schema\n        processors:\n          - type: turms.processors.disclaimer.DisclaimerProcessor\n          - type: turms.processors.black.BlackProcessor\n          - type: turms.processors.isort.IsortProcessor\n          - type: turms.processors.merge.MergeProcessor # merges the formated schema with already defined functions\n        scalar_definitions:\n          uuid: str\n          _Any: typing.Any\n```\n\n### Usage\n\nOnce you have configured turms you can generate your code by running\n\n```bash\nturms gen\n```\n\n### Why Turms\n\nIn Etruscan religion, Turms (usually written as 𐌕𐌖𐌓𐌌𐌑 Turmś in the Etruscan alphabet) was the equivalent of Roman Mercury and Greek Hermes, both gods of trade and the **messenger** god between people and gods.\n\n## Transport Layer\n\nTurms does _not_ come with a default transport layer but if you are searching for an Apollo-like GraphQL Client you can check out [rath](https://github.com/jhnnsrs/rath), that works especially well with turms.\n\n## Examples\n\nThis github repository also contains some examples on how to use turms with popular libraries in the graphql ecosystem.\n',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://jhnnsrs.github.io/turms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
