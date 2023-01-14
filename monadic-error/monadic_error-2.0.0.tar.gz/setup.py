# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monadic_error']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monadic-error',
    'version': '2.0.0',
    'description': 'Monads used for handling Errors. Contains Attempt and Option.',
    'long_description': '# Monadic Error\nby Ian Kollipara\n\n\nThis is a small library containing 2 monads for handling errors in Python: Attempt (Either) and Option (Maybe).\nThese two are chosen for their usefulness in handling errors gracefully, and for the ability to slot in nicely with python.\nBoth monads work with Python 3.10 pattern matching, and as well as MyPy exhaustive pattern matching.\n\nAll monads implement `map`, `flatMap`, and `unwrap_or`. These all aid in their use in python.\nIn addition there are a few utility functions for working with the objects during the execution of the program.\n\n## Attempt\n\nAttempt is the Either monad. The name was chosen to signify how it should be used.\nThere are two constructors for this: Success and Failure.\nUse them as their name denotes.\n\n## Option\n\nOption is the Maybe Monad. The name was chosen to signify how it should be used.\nThere are two constructors for this: Some and Nothing.\nUse them as their name denotes.\n\n',
    'author': 'Ian Kollipara',
    'author_email': 'ian.kollipara@cune.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
