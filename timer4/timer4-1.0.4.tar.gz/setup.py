# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'timer4',
    'version': '1.0.4',
    'description': 'Timing Python code made easy',
    'long_description': '# timer ![PyPI](https://img.shields.io/pypi/v/timer4) ![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)\n\n`timer` is a library to time your Python code.\n\n## Installation\n\n```bash\npip install timer4  # not timer\n```\n\n## Usage\n\n- `timer` uses `with` statement to watch how long your code running:\n\n```python\nimport time\nfrom timer import Timer\n\n\nwith Timer().watch_and_report(msg=\'test\'):\n    # running code that do lots of computation\n    time.sleep(1.0)\n\n# when the code reach this part, it will output the message and the time it tooks.\n# for example:\n#     test: 10.291 seconds\n```\n\n- If you don\'t want to report the result immediately, use the `watch` method instead. Whenever you\'ve done, call `report`.\n\n```python\nimport time\nfrom timer import Timer\n\n# you can either create a timer variable first, or use Timer.get_instance()\n# that will return a singleton variable.\n\ntotal = 0\nfor item in range(7):\n    # only measure the part that we want\n    with Timer.get_instance().watch("sum of square"):\n        total += item ** 2\n        time.sleep(0.2)\n\n    # doing other things that we don\'t want to measure\n    time.sleep(0.8)\n\nTimer.get_instance().report()\n```\n\n- You can also use different way to print the message, such as using logging by passing a printing function to the report method: `report(print_fn=logger.info)`\n\n- You can also choose to append the result to a file `report(append_to_file=\'/tmp/runtime.csv\')`. This is useful if you want to measure runtime of your method and put it to a file to plot it later.\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
