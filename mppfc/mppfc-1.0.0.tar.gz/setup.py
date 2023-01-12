# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mppfc']

package_data = \
{'': ['*']}

install_requires = \
['binfootprint>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'mppfc',
    'version': '1.0.0',
    'description': 'multi-processing persistent function cache',
    'long_description': '# mppfc - Multi-Processing Persistent Function Cache\n\nThe `mppfc` module allows to speed up the evaluation of computationally \nexpansive functions by \na) processing several arguments in parallel and \nb) persistent caching of the results to disk.\nPersistent caching becomes available by simply decorating a given function.\nWith no more than two extra lines of code, parallel evaluation is realized.\n\nHere is a [minimal example](./examples/minimal.py):\n\n```python\nimport mppfc\n\n@mppfc.MultiProcCachedFunctionDec()\ndef slow_function(x):\n    # complicated stuff\n    return x\n\nslow_function.start_mp()\nfor x in some_range:\n    y = slow_function(x)\nslow_function.wait()\n```\nThe first time you run this script, all `y` are `None`, since the evaluation \nis done by several background processes.\nOnce `wait()` returns, all parameters have been cached to disk.\nSo calling the script a second time yields (almost immediately) the\ndesired results in `y`.\n\nEvaluating only the `for` loop in a jupyter notebook cell\nwill give you partial results if the background processes are still doing some work.\nIn that way you can already show successfully retrieved results.\n(see the examples [simple.ipynb](./examples/simple.ipynb) and [live_update.ipynb](./examples/live_update.ipynb))\n\nFor a nearly exhaustive example see [full.py](./examples/full.py).\n\n### pitfalls\n\nNote that arguments are distinguished by their binary representation obtained from the \n[binfootprint](https://github.com/richard-hartmann/binfootprint) module.\nThis implies that the integer `1` and the float `1.0` are treated as different arguments, even though\nin many numeric situations the result does not differ.\n\n```python\nimport mppfc\nimport math\n\n@mppfc.MultiProcCachedFunctionDec()\ndef pitfall_1(x):\n    return math.sqrt(x)\n\nx = 1\nprint("pitfall_1(x={}) = {}".format(x, pitfall_1(x=x)))\n# pitfall_1(x=1) = 1.0\nx = 1.0\nprint("BUT, x={} in cache: {}".format(x, pitfall_1(x=x, _cache_flag="has_key")))\n# BUT, x=1.0 in cache: False\nprint("and obviously: pitfall_1(x={}) = {}".format(x, pitfall_1(x=x, _cache_flag="no_cache")))\n# and obviously: pitfall_1(x=1.0) = 1.0\n```\n\nThe same holds true for lists and tuples.\n\n```python\nimport mppfc\nimport math\n\n@mppfc.MultiProcCachedFunctionDec()\ndef pitfall_2(arr):\n    return sum(arr)\n\narr = [1, 2, 3]\nprint("pitfall_2(arr={}) = {}".format(arr, pitfall_2(arr=arr)))\n# pitfall_2(arr=[1, 2, 3]) = 6\narr = (1, 2, 3)\nprint("BUT, arr={} in cache: {}".format(arr, pitfall_2(arr=arr, _cache_flag="has_key")))\n# BUT, arr=(1, 2, 3) in cache: False\nprint("and obviously: pitfall_1(arr={}) = {}".format(arr, pitfall_2(arr=arr, _cache_flag="no_cache")))\n# and obviously: pitfall_1(arr=(1, 2, 3)) = 6\n```\n\nFor more details see [binfootprint\'s README](https://github.com/richard-hartmann/binfootprint).\n\n## Installation\n\n### pip\n\n    pip install mppfc\n\n### poetry\n\nUsing poetry allows you to include this package in your project as a dependency.\n\n### git\n\ncheck out the code from github\n\n    git clone https://github.com/richard-hartmann/mppfc.git\n\n## Dependencies\n\n - requires at least python 3.8\n - uses [`binfootprint`](https://github.com/richard-hartmann/binfootprint) \n   to serialize and hash the arguments of a function \n\n## Licence\n\n### MIT licence\nCopyright (c) 2023 Richard Hartmann\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Richard Hartmann',
    'author_email': 'richard_hartmann@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
