# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delegatefn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'delegatefn',
    'version': '0.4.0',
    'description': 'Signature-preserving function delegation',
    'long_description': '# delegatefn\n\nA Python package for adding the parameters of a delegatee function to a delegator function, while keeping the original parameters of the delegator function.\n\n## Installation\n\nTo install `delegatefn`, use `pip`:\n\n```bash\npip install delegatefn\n```\n\n## Usage\n\nTo use the `delegate` decorator function, import it from `delegatefn`:\n\n```python\nfrom delegatefn import delegate\n```\n\nThen, decorate your delegator function with the `delegate` decorator, passing in the delegatee function as an argument:\n\n```python\n@delegate(delegatee)\ndef delegator(c: int, d: int, e: int, **kwargs):\n    ...\n```\n\nThe delegator function will now have the parameters of delegatee added to it, while keeping its original parameters.\n\nYou can also customize the behavior of the `delegate` decorator by passing in the following keyword arguments:\n\n- `kwonly`: A boolean value indicating whether the parameters of delegatee should be converted to keyword-only arguments. The default value is `True`.\n\n- `delegate_docstring`: A boolean value indicating whether the docstring of delegatee should be used as the docstring of the delegator function. The default value is `True`.\n\n- `ignore`: A set of strings containing the names of the parameters of delegatee that should be ignored. The default value is an empty set.\n\nHere is an example of how to use these keyword arguments:\n\n```python\n@delegate(delegatee, kwonly=True, delegate_docstring=True, ignore={"a", "b"})\ndef delegator(c: int, d: int, e: int, **kwargs):\n    ...\n```\n\n## Example\n\nHere is an example of how to use the `delegate` decorator:\n\n```python\nfrom delegatefn import delegate\n\ndef delegatee(a: int, b: int, **kwargs):\n    ...\n\n@delegate(delegatee)\ndef delegator(c: int, d: int, e: int, **kwargs):\n    ...\n```\n\nThe delegator function will now have the parameters `a: int`, `b: int`, and `kwargs` added to it, in addition to its original parameters `c: int`, `d: int`, and `e: int`.\n\n## Acknowledgements\n\nThis approach was inspired by [fast.ai](https://www.fast.ai/posts/2019-08-06-delegation.html).\n',
    'author': 'IsaacBreen',
    'author_email': '57783927+IsaacBreen@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
