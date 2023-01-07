# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peaceful_pie']

package_data = \
{'': ['*']}

install_requires = \
['chili>=1.8.0,<2.0.0', 'numpy>=1.24.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'peaceful-pie',
    'version': '1.5.0',
    'description': 'Control Unity from Python!',
    'long_description': '# Peaceful Pie\n\nConnect Python with Unity for reinforcement learning!\n\n# CI\n\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hughperkins/peaceful-pie/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/hughperkins/peaceful-pie/tree/main)\n\n# Examples\n\n- see [examples](examples)\n\n# Installation\n\nYou need to install both into Unity project, and into your Python environment.\n\n## In Unity\n\n- In Unity, go to Window | Package Manager\n    - change the dropdown in top left to \'Packages: In Project\'\n    - check that Newtonsoft Json appears\n    - if Newtonsoft Json is not already in your project:\n        - click on the \'+\' in the top left, and choose \'Add package by name...\'\n        - put the name `com.unity.nuget.newtonsoft-json`, then click \'Add\'\n- In Unity, in your project\'s "Assets" folder, create a "Plugins" folder, if it doesn\'t already exist\n- First install AustinHarris.JsonRPC:\n    - Download https://www.nuget.org/api/v2/package/AustinHarris.JsonRpc/1.2.3\n    - rename to have filename suffix be `.zip` (you might need to turn on options to see all file extensions)\n    - unzip the resulting zip file\n    - copy `lib/netstandard2.1/AustinHarris.JsonRpc.dll` into your `Plugins` folder\n    - select the file, in your Plugins, and in \'Inspector\' unselect \'validate references\', and click \'Apply\'\n- Click on \'Releases\', on the right of the github page\n    - in the most recent release, download `PeacefulPie.dll`\n- Copy `PeacefulPie.dll` into your Unity project\'s `Plugins` folder\n- If on Mac silicon:\n    - in Unity, goto Plugins, click on `PeacefulPie.dll`\n    - in Inspector, change \'CPU\' setting from \'Intel\' to \'Any CPU\', then click \'Apply\'\n    - do the same for `AustinHarris.JsonRpc.dll`\n\nYou should be good to go :)\n\n## In Python\n\n```\npip install -U peaceful-pie\n```\n\n# Requirements\n\n- currently tested with:\n    - python 3.10\n    - Unity 2021.3.16.f1\n- please create an issue if your preferred platform is not supported (I\'m guessing I might need to downgrade Python a little? Let me know!)\n\n# Dev\n\nI\'m usng Visual Studio for Mac to write this.\n',
    'author': 'Hugh Perkins',
    'author_email': 'hughperkins@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hughperkins/peaceful-pie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
