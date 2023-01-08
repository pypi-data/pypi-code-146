# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haxballgym',
 'haxballgym.envs',
 'haxballgym.utils',
 'haxballgym.utils.action_parsers',
 'haxballgym.utils.gamestates',
 'haxballgym.utils.obs_builders',
 'haxballgym.utils.reward_functions',
 'haxballgym.utils.reward_functions.common_rewards',
 'haxballgym.utils.terminal_conditions']

package_data = \
{'': ['*']}

install_requires = \
['gym==0.21', 'numpy>=1.23.5,<2.0.0', 'ursinaxball==0.1.3']

setup_kwargs = {
    'name': 'haxballgym',
    'version': '0.4.1',
    'description': 'HaxBallGym is a python package that can be used to treat the game HaxBall as though it were an OpenAI-style environment for Reinforcement Learning projects.',
    'long_description': "# HaxBallGym\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nHaxBallGym is a Python package that can be used to treat the game [HaxBall](https://www.haxball.com) as though it were an [OpenAI Gym](https://gym.openai.com)-style environment for Reinforcement Learning projects.\n\n## Requirements\n\n- Python >= 3.10\n\n## Installation\n\nInstall the library via pip:\n\n```bash\npip install haxballgym\n```\n\nThat's it! Run `example.py` to see if the installation was successful. The script assumes you have a recordings folder from where you run the script.\n\n## Recordings\n\nTo watch recordings, go to my [HaxBall clone](https://wazarr94.github.io/) and load the recording file.\n\n## Discord\n\n[![Join our Discord server!](https://invidget.switchblade.xyz/TpKPeCe7y6)](https://discord.gg/TpKPeCe7y6)\n",
    'author': 'Wazarr',
    'author_email': 'jeje_04@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
