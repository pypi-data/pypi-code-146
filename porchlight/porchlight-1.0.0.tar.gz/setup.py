# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['porchlight', 'porchlight.tests', 'porchlight.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'porchlight',
    'version': '1.0.0',
    'description': 'A function-managing package for models and systems with shared variables.',
    'long_description': '<img src="docs/source/porchlight_logo.gif" width="200" height="200" alt="porchlight logo. A snake\'s head erupts from the bottom of a porchlight casing, reaching towards a spinning triangular pyramid. The pyramid radiates bright, saturated, multicolored light." style="float:left" />\n\n[porchlight](https://porchlight.readthedocs.io/en/latest/)\n==========\n\n`porchlight` is a function management suite that handles shared inputs and\noutputs of methods and/or functions which evolve over the lifetime of a program.\n\nThis package\'s original intent was to be a part of a modular scientific package\nyet to be released. Rather than isolating this method to a single model, the\nalready-developed work has been modified to stand alone as a package.\n\n`porchlight` does not have any dependencies outside of the standard CPython\nlibrary. Please note that `porchlight` requires Python 3.9\\+, and that examples\nmay require external libraries such as `numpy` and `matplotlib`.\n\nInstallation\n------------\n\nYou can install `porchlight` by cloning this repository to a local directory,\nopening a command line, and running:\n```pip install porchlight```\n\nUsage\n-----\n\nThe main object used in `porchlight` is the `porchlight.Neighborhood` object.\nThis groups all functions together and keeps track of call order and\nparameters.\n\n```python\nimport porchlight\n\n\n# To add a function, we simply define it and pass it to porchlight.\ndef increase_x(x: int, y: int) -> int:\n    x = x * y\n    return x\n\n# Type annotations are optional, as with normal python.\ndef string_x(x):\n    x_string = f"{x = }"\n    return x_string\n\ndef increment_y(y=0):\n    y = y + 1\n    return y\n\n# Generating a complete, coupled model between these functions is as simple as\n# adding all these functions to a Neighborhood object.\nneighborhood = Neighborhood([increment_y, increase_x, string_x])\n\n# The neighborhood object inspects the function, finding input and output\n# variables if present. These are added to the collections of functions and\n# parameters.\nprint(neighborhood)\n\n# We initialize any variables we need to (in this case, just x), and then\n# executing the model is a single method call.\nneighborhood.set_param(\'x\', 2)\n\nneighborhood.run_step()\n\n# Print out information.\nfor name, param in neighborhood.params.items():\n    print(f"{name} = {param}")\n```\n\nDocumentation\n-----------\n\nDocumentation for `porchlight` can be found on Read the Docs here: https://porchlight.readthedocs.io/en/latest/\n',
    'author': 'Teal, D',
    'author_email': 'teal.dillon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
