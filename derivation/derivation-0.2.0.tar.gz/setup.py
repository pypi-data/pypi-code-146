# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['derivation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'derivation',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Derivation\n\n[![Maintainability](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/maintainability)](https://codeclimate.com/github/RainrainWu/derivation/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/test_coverage)](https://codeclimate.com/github/RainrainWu/derivation/test_coverage)\n[![codecov](https://codecov.io/gh/RainrainWu/derivation/branch/master/graph/badge.svg?token=at8Ckp5iLi)](https://codecov.io/gh/RainrainWu/derivation)\n[![Github Actions](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml/badge.svg)](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)\n\nDerivation is a flexible payload generating framework with highly-customizable patterns and rules which raise your efficiency significantly on test case implementation against complicated inputs.\n\n## Getting Started\n\n### Derivative\n\nDerivative is the primary object which sorted out all of valid outputs meet the constraints.\n\n> The script below can be executed directly\n```python\nfrom enum import Enum, auto\nfrom operator import or_\n\nfrom derivation.constraint import (\n    MutuallyExclusiveConstraint,\n    OccurrenceConstraint,\n    PrerequisiteConstraint,\n    TerminationConstraint,\n)\nfrom derivation.derivative import Derivative\n\n\nclass DerivativeEvent(Enum):\n    @staticmethod\n    def _generate_next_value_(name, start, count, last_values):\n        return name.upper()\n\n\nclass DerivativeEventAlpha(DerivativeEvent):\n\n    ESSENTIALS = auto()\n\n    OPTIONAL_1 = auto()\n    OPTIONAL_1_1 = auto()\n    OPTIONAL_1_2 = auto()\n\n    OPTIONAL_2 = auto()\n    OPTIONAL_3 = auto()\n\n\nEVENT_ALPHA = {event: {event.value: None} for event in DerivativeEventAlpha}\n\nderivative = Derivative(\n    EVENT_ALPHA,\n    or_,\n    (\n        OccurrenceConstraint(\n            (DerivativeEventAlpha.ESSENTIALS,),\n            min_times=1,\n            max_times=1,\n        ),\n        MutuallyExclusiveConstraint(\n            (\n                DerivativeEventAlpha.OPTIONAL_1,\n                DerivativeEventAlpha.OPTIONAL_2,\n                DerivativeEventAlpha.OPTIONAL_3,\n            ),\n        ),\n        MutuallyExclusiveConstraint(\n            (DerivativeEventAlpha.OPTIONAL_1_1, DerivativeEventAlpha.OPTIONAL_1_2),\n        ),\n        PrerequisiteConstraint(\n            (DerivativeEventAlpha.OPTIONAL_1,),\n            (DerivativeEventAlpha.OPTIONAL_1_1, DerivativeEventAlpha.OPTIONAL_1_2),\n        ),\n        TerminationConstraint(\n            {\n                DerivativeEventAlpha.OPTIONAL_1_1,\n                DerivativeEventAlpha.OPTIONAL_1_2,\n                DerivativeEventAlpha.OPTIONAL_2,\n                DerivativeEventAlpha.OPTIONAL_3,\n            },\n        ),\n    ),\n)\n\nfor order, result in derivative.exhaustive():\n\n    print(f"{order}\\n{result}\\n")\n```',
    'author': 'Rain Wu',
    'author_email': 'rain.wu@appier.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
