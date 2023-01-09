# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['urdfenvs',
 'urdfenvs.keyboard_input',
 'urdfenvs.robots.albert',
 'urdfenvs.robots.boxer',
 'urdfenvs.robots.generic_urdf',
 'urdfenvs.robots.iris',
 'urdfenvs.robots.jackal',
 'urdfenvs.robots.prius',
 'urdfenvs.robots.tiago',
 'urdfenvs.scene_examples',
 'urdfenvs.sensors',
 'urdfenvs.urdf_common']

package_data = \
{'': ['*'],
 'urdfenvs.robots.albert': ['meshes/*',
                            'meshes/collision/*',
                            'meshes/visual/*'],
 'urdfenvs.robots.boxer': ['meshes/collision/*', 'meshes/visual/*'],
 'urdfenvs.robots.generic_urdf': ['dual_arm/*',
                                  'mobile_panda/*',
                                  'mobile_panda/meshes/collision/*',
                                  'mobile_panda/meshes/visual/*',
                                  'n_link/*',
                                  'panda/*',
                                  'panda/meshes/collision/*',
                                  'panda/meshes/visual/*',
                                  'point_robot/*'],
 'urdfenvs.robots.iris': ['meshes/*'],
 'urdfenvs.robots.jackal': ['meshes/*',
                            'meshes/collision/*',
                            'meshes/visual/*'],
 'urdfenvs.robots.prius': ['meshes/*'],
 'urdfenvs.robots.tiago': ['pal_gripper_description/meshes/*',
                           'pmb2_description/meshes/base/*',
                           'pmb2_description/meshes/meshes/*',
                           'pmb2_description/meshes/objects/*',
                           'pmb2_description/meshes/sensors/*',
                           'pmb2_description/meshes/wheels/*',
                           'tiago_description/meshes/arm/*',
                           'tiago_description/meshes/head/*',
                           'tiago_description/meshes/sensors/xtion_pro_live/*',
                           'tiago_description/meshes/torso/*',
                           'tiago_dual_description/meshes/torso/*'],
 'urdfenvs.scene_examples': ['obstacle_data/*'],
 'urdfenvs.urdf_common': ['meshes/*']}

install_requires = \
['gym>=0.21.0,<0.22.0',
 'numpy>=1.19,<1.24',
 'pybullet>=3.2.1,<4.0.0',
 'urdfpy>=0.0.22,<0.0.23']

extras_require = \
{'keyboard': ['pynput>=1.7.6,<2.0.0', 'multiprocess>=0.70.12,<0.71.0'],
 'scenes': ['motion-planning-scenes>=0.3.4,<0.4.0']}

setup_kwargs = {
    'name': 'urdfenvs',
    'version': '0.4.2',
    'description': 'Simple simulation environment for robots, based on the urdf files.',
    'long_description': 'Generic URDF robots\n===================\n\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/maxspahn/gym_envs_urdf.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/maxspahn/gym_envs_urdf/context:python)\n\n### Generic URDF robots\n\nIn this package, generic urdf robots and a panda gym environment are available.\nThe goal is to make this environment as easy as possible to deploy. Although, we used the\nOpenAI-Gym framing, these environments are not necessarly restricted to\nReinforcement-Learning but rather to local motion planning in general.\n\n<table>\n <tr>\n  <td> Point Robot </td>\n  <td> Point Robot with Keyboard Input </td>\n  <td> Non-Holonomic Robot </td>\n </tr>\n <tr>\n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/pointRobot.gif" width="250" height="250"/> </td>\n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/pointRobotKeyboardInput.gif" width="250" height="250"/> </td>  \n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/boxerRobot.gif" width="250" height="250"/> </td>\n </tr>\n</table>\n\n<table>\n <tr>\n  <td> Tiago Robot </td>\n  <td> Tiago Robot with Keyboard Input </td>\n </tr>\n <tr>\n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/tiago.gif" width="250" height="250"/> </td>\n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/tiagoKeyboardInput.gif" width="250" height="250"/> </td>\n </tr>\n</table>\n\n<table>\n <tr>\n  <td> Panda Robot </td>\n  <td> Albert Robot </td>\n  </tr>\n <tr>\n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/panda.gif" width="250" height="250"/> </td>\n  <td> <img src="https://raw.githubusercontent.com/maxspahn/gym_envs_urdf/master/docs/source/img/albert.gif" width="250" height="250"/> </td>\n  </tr>\n</table>\n\nGetting Started\n================\n\nThis is the guide to quickle get going with urdf gym environments.\n\nPre-requisites\n==============\n\n-   Python &gt;3.6, &lt;3.10\n-   pip3\n-   git\n\nInstallation\n============\n\nYou first have to downlad the repository\n\n``` {.sourceCode .bash}\ngit clone git@github.com:maxspahn/gym_envs_urdf.git\n```\n\nThen, you can install the package using pip as:\n\n``` {.sourceCode .bash}\npip3 install .\n```\n\nOptional: Installation with poetry\n==================================\n\nIf you want to use [poetry](https://python-poetry.org/docs/), you have\nto install it first. See their webpage for instructions\n[docs](https://python-poetry.org/docs/). Once poetry is installed, you\ncan install the virtual environment with the following commands. Note\nthat during the first installation `poetry update` takes up to 300 secs.\n\n``` {.sourceCode .bash}\npoetry install\n```\n\nThe virtual environment is entered by\n\n``` {.sourceCode .bash}\npoetry shell\n```\n\nInside the virtual environment you can access all the examples.\n\nExamples\n========\n\nRun example\n-----------\n\nYou find several python scripts in\n[examples/](https://github.com/maxspahn/gym_envs_urdf/tree/master/examples).\nYou can test those examples using the following (if you use poetry, make\nsure to enter the virtual environment first with `poetry shell`)\n\n``` {.sourceCode .python}\npython3 point_robot.py\n```\n\nReplace point_robot.py with the name of the script you want to run.\n\nUse environments\n----------------\n\nIn the `examples`, you will find individual examples for all implemented\nrobots. Environments can be created using the normal gym syntax. Gym\nenvironments rely mostly on three functions\n\n-   `gym.make(...)` to create the environment,\n-   `gym.reset(...)` to reset the environment,\n-   `gym.step(action)` to step one time step in the environment.\n\nFor example, in\n[examples/point_robot.py](https://github.com/maxspahn/gym_envs_urdf/blob/master/examples/point_robot.py),\nyou can find the following syntax to `make`, `reset` and `step` the\nenvironment.\n\n``` {.sourceCode .python}\nenv = gym.make(\'pointRobotUrdf-vel-v0\', dt=0.05, render=True)\nob = env.reset(pos=pos0, vel=vel0)\nob, reward, done, info = env.step(action)\n```\n\nThe id-tag in the `make` command specifies the robot and the control\ntype. You can get a full list of all available environments using\n\n``` {.sourceCode .python}\nfrom gym import envs\nprint(envs.registry.all())\n```\n\nGo ahead and explore all the examples you can find there.\n',
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': 'Max Spahn',
    'maintainer_email': 'm.spahn@tudelft.nl',
    'url': 'https://maxspahn.github.io/gym_envs_urdf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.5,<3.10',
}


setup(**setup_kwargs)
