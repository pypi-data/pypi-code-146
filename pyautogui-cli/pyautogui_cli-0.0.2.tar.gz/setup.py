# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyautogui_cli']

package_data = \
{'': ['*']}

install_requires = \
['pyautogui>=0.9.53,<0.10.0']

entry_points = \
{'console_scripts': ['pyautogui = pyautogui_cli.main:main']}

setup_kwargs = {
    'name': 'pyautogui-cli',
    'version': '0.0.2',
    'description': '',
    'long_description': '# pyautogui-cli\n\n## Usage\n\nPutting the function name of `pyautogui` as the first argument, and all the arguments (anything inside the parentheses) as the second.\n\n### Example\n\n`pyautogui.moveTo()`:\n\n```\n>>> pyautogui.moveTo(100, 200)  # moves mouse to X of 100, Y of 200.\n```\n\nshould be translated as:\n\n```\n$ pyautogui moveTo "100, 200"\n```\n',
    'author': 'Johann Chang',
    'author_email': 'mr.changyuheng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/changyuheng/pyautogui-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
