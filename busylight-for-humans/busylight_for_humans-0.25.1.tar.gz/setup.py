# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['busylight',
 'busylight.api',
 'busylight.effects',
 'busylight.lights',
 'busylight.lights.agile_innovative',
 'busylight.lights.compulab',
 'busylight.lights.embrava',
 'busylight.lights.kuando',
 'busylight.lights.luxafor',
 'busylight.lights.muteme',
 'busylight.lights.mutesync',
 'busylight.lights.plantronics',
 'busylight.lights.thingm']

package_data = \
{'': ['*']}

install_requires = \
['bitvector-for-humans>=0.14.0,<0.15.0',
 'hidapi>=0.13.1,<0.14.0',
 'loguru>=0.6.0,<0.7.0',
 'pyserial>=3.5,<4.0',
 'typer>=0.7.0,<0.8.0',
 'webcolors>=1.11.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.11.3,<7.0.0']}

entry_points = \
{'console_scripts': ['busylight = busylight.__main__:cli',
                     'busyserve = busylight.__main__:webcli']}

setup_kwargs = {
    'name': 'busylight-for-humans',
    'version': '0.25.1',
    'description': 'Control USB connected LED lights, like a human.',
    'long_description': '<!-- USB HID API embrava blynclight agile innovative blinkstick kuando busylight omega alpha plantronics luxafor bluetooth bt flag mute orb thingM blink(1) muteme mutesync compulab fit-statusb -->\n![BusyLight Project Logo][LOGO]\n<br>\n![version][pypi-version]\n![monthly-downloads][monthly-downloads]\n![visits][visits]\n![supported python versions][python-versions] \n![license][license]\n![Code style: black][code-style-black]\n<br>\n[![pytest-linux](https://github.com/JnyJny/busylight/actions/workflows/pytest-linux.yaml/badge.svg)](https://github.com/JnyJny/busylight/actions/workflows/pytest-linux.yaml)\n[![MacOS](https://github.com/JnyJny/busylight/actions/workflows/pytest-macos.yaml/badge.svg)](https://github.com/JnyJny/busylight/actions/workflows/pytest-macos.yaml)\n[![pytest-windows](https://github.com/JnyJny/busylight/actions/workflows/pytest-windows.yaml/badge.svg)](https://github.com/JnyJny/busylight/actions/workflows/pytest-windows.yaml)\n<br>\n\n[BusyLight for Humans™][0] gives you control of USB attached LED\nlights from a variety of vendors. Lights can be controlled via\nthe command-line, using a HTTP API or imported directly into your own\nPython project.\n\n![All Supported Lights][DEMO]\nFlag<sup>1</sup>,\nBusylight Alpha<sup>2</sup>,\nStatus Indicator<sup>3</sup>,\nBlink(1)<sup>4</sup>,\nMute<sup>5</sup>,\nBlynclight<sup>6</sup>.\nOrb<sup>7</sup>,\nBusyLight Omega<sup>8</sup>,\nBlinkStick Square<sup>9</sup>,\nBlynclight Mini<sup>10</sup>,\nMuteMe Original<sup>11</sup>,\nfit-statUSB<sup>12</sup>,\nMuteSync<sup>13</sup>, \nBlynclight Plus<sup>14</sup>\n\n## Features\n- Control lights from the [command-line][HELP].\n- Control lights via a [Web API][WEBAPI].\n- Import `busylight` into your own Python project.\n- Supported on MacOS and Linux\n- Windows support is untested but there are reports that it is working.\n- Supports _nine_ vendors & sixteen devices:\n\n| **Vendor** | | | |\n|------------:|---|---|---|\n| [**Agile Innovative**][2] | BlinkStick Square |\n| [**Compulab**][8] | fit-statUSB |\n| [**Embrava**][3] | Blynclight | Blynclight Mini | Blynclight Plus |\n| [**Kuando**][4] | Busylight Alpha | BusyLight Omega |\n| [**Luxafor**][5] | Bluetooth | Flag | Mute | Orb |\n| [**Plantronics**][3] | Status Indicator |\n| [**MuteMe**][7] | MuteMe Original | Mute Mini |\n| [**MuteSync**][9] | MuteSync |\n| [**ThingM**][6] | Blink(1) |\n\nIf you have a USB light that\'s not on this list open an issue with:\n - the make and model device you want supported\n - where I can get one\n - any public hardware documentation you are aware of\n \nOr even better, open a pull request!\n\n### Gratitude\n\nThank you to [@todbot][todbot] and the very nice people at [ThingM][thingm] who\ngraciously and unexpectedly gifted me with two `blink(1) mk3` lights!\n\n## Basic Install\n\nInstalls only the command-line `busylight` tool and associated\nmodules.\n\n```console\n$ python3 -m pip install busylight-for-humans \n```\n\n## Web API Install\n\nInstalls `uvicorn` and `FastAPI` in addition to `busylight`:\n\n```console\n$ python3 -m pip install busylight-for-humans[webapi]\n```\n\n## Development Install\n\nI use the tool [poetry][poetry-docs] to manage various aspects of this project, including:\n- dependencies\n- pytest configuration\n- versioning\n- optional dependencies\n- virtual environment creation\n- building packages\n- publishing packages to PyPi\n\n```console\n$ python3 -m pip install poetry \n$ cd path/to/busylight\n$ poetry shell\n<venv> $ poetry install -E webapi\n<venv> $ which busylight\n<venv> $ which busyserve\n```\n\nAfter installing into the virtual environment, the project is now available in editable mode.  Changes made in the source will be reflected in the runtime behavior when running in the poetry initiated shell.\n\n## Linux Post-Install Activities\n\nLinux controls access to USB devices via the [udev subsystem][UDEV]. By\ndefault it denies non-root users access to devices it doesn\'t\nrecognize. I\'ve got you covered!\n\nYou\'ll need root access to configure the udev rules:\n\n```console\n$ busylight udev-rules -o 99-busylights.rules\n$ sudo cp 99-busylights.rules /etc/udev/rules.d\n$ sudo udevadm control -R\n$ # unplug/plug your light\n$ busylight on\n```\n\n## Command-Line Examples\n\n```console\n$ busylight on               # light turns on green\n$ busylight on red           # now it\'s shining a friendly red\n$ busylight on 0xff0000      # still red\n$ busylight on #00ff00       # now it\'s blue!\n$ busylight blink            # it\'s slowly blinking on and off with a red color\n$ busylight blink green fast # blinking faster green and off\n$ busylight --all on         # turn all lights on green\n$ busylight --all off        # turn all lights off\n```\n\n## HTTP API Examples\n\nFirst start the `busylight` API server using the `busyserv` command line interface:\n```console\n$ busyserve -D\nINFO:     Started server process [40064]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\nINFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)\n...\n```\n\nThe API is fully documented and available via these URLs:\n\n- `https://localhost:8000/redoc`\n- `https://localhost:8000/docs`\n\n\nNow you can use the web API endpoints which return JSON payloads:\n\n```console\n  $ curl -s http://localhost:8000/lights/status | jq\n  ...\n  $ curl -s http://localhost:8000/light/0/status | jq\n  ...\n  $ curl -s http://localhost:8000/light/0/on | jq\n  {\n    "light_id": 0,\n    "action": "on",\n    "color": "green",\n\t"rgb": [0, 128, 0]\n  }\n  $ curl -s http://localhost:8000/light/0/off | jq\n  {\n    "light_id": 0,\n    "action": "off"\n  }\n  $ curl -s http://localhost:8000/light/0/on?color=purple | jq\n  {\n    "light_id": 0,\n    "action": "on",\n    "color": "purple",\n\t"rgb": [128, 0, 128]\n  }\n  $ curl -s http://localhost:8000/lights/on | jq\n  {\n    "light_id": "all",\n    "action": "on",\n    "color": "green",\n\t"rgb", [0, 128, 0]\n  }\n  $ curl -s http://localhost:8000/lights/off | jq\n  {\n    "light_id": "all",\n    "action": "off"\n  }\n  $ curl -s http://localhost:8000/lights/rainbow | jq\n  {\n    "light_id": "all",\n    "action": "effect",\n    "name": "rainbow"\n  }\n```\n\n### Authentication\nThe API can be secured with a simple username and password through\n[HTTP Basic Authentication][BASICAUTH]. To require authentication\nfor all API requests, set the `BUSYLIGHT_API_USER` and\n`BUSYLIGHT_API_PASS` environmental variables before running\n`busyserve`.\n\n> :warning: **SECURITY WARNING**: HTTP Basic Auth sends usernames and passwords in *cleartext* (i.e., unencrypted). Use of SSL is highly recommended!\n\n## Code Examples\n\nAdding light support to your own python applications is easy!\n\n### Simple Case: Turn On a Single Light\n\nIn this example, we pick an Embrava Blynclight to activate with\nthe color white. \n\n```python\nfrom busylight.lights.embrava import Blynclight\n\nlight = Blynclight.first_light()\n\nlight.on((255, 255, 255))\n```\n\nNot sure what light you\'ve got? \n\n```python\nfrom busylight.lights import USBLight\n\nlight = USBLight.first_light()\n\nlight.on((0xff, 0, 0xff))\n```\n\n### Slightly More Complicated\n\nThe `busylight` package includes a manager class that\'s great for\nworking with multiple lights or lights that require a little\nmore direct intervention like the Kuando Busylight family.\n\n```python\nfrom busylight.manager import LightManager\nfrom busylight.effects import Effects\n\nmanager = LightManager()\nfor light in manager.lights:\n   print(light.name)\n   \nrainbow = Effects.for_name("spectrum")(duty_cycle=0.05)\n\nmanager.apply_effect(rainbow)\n...\nmanager.off()\n```\n\n[0]: https://github.com/JnyJny/busylight\n\n\n<!-- doc links -->\n[2]: https://github.com/JnyJny/busylight/blob/master/docs/devices/agile_innovative.md\n[3]: https://github.com/JnyJny/busylight/blob/master/docs/devices/embrava.md\n[4]: https://github.com/JnyJny/busylight/blob/master/docs/devices/kuando.md\n[5]: https://github.com/JnyJny/busylight/blob/master/docs/devices/luxafor.md\n[6]: https://github.com/JnyJny/busylight/blob/master/docs/devices/thingm.md\n[7]: https://github.com/JnyJny/busylight/blob/master/docs/devices/muteme.md\n[8]: https://github.com/JnyJny/busylight/blob/master/docs/devices/compulab.md\n[9]: https://github.com/JnyJny/busylight/blob/master/docs/devices/mutesync.md\n\n[LOGO]: https://github.com/JnyJny/busylight/blob/master/docs/assets/BusyLightForHumans.png\n[HELP]: https://github.com/JnyJny/busylight/blob/master/docs/busylight.1.md\n[WEBAPI]: https://github.com/JnyJny/busylight/blob/master/docs/busylight_api.pdf\n\n<!-- [DEMO]: demo/demo-updated.gif -->\n[DEMO]: https://github.com/JnyJny/busylight/blob/master/docs/assets/HerdOfLights.png\n\n[BASICAUTH]: https://en.wikipedia.org/wiki/Basic_access_authentication\n[UDEV]: https://en.wikipedia.org/wiki/Udev\n\n[todbot]: https://github.com/todbot\n[thingm]: https://thingm.com\n\n<!-- badges -->\n\n[code-style-black]: https://img.shields.io/badge/code%20style-black-000000.svg\n[pypi-version]: https://img.shields.io/pypi/v/busylight-for-humans\n[python-versions]: https://img.shields.io/pypi/pyversions/busylight-for-humans\n[license]: https://img.shields.io/pypi/l/busylight-for-humans\n[dependencies]: https://img.shields.io/librariesio/github/JnyJny/busylight\n[monthly-downloads]: https://img.shields.io/pypi/dm/busylight-for-humans\n[poetry-docs]: https://python-poetry.org/docs/\n[visits]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJnyJny%2Fbusylight&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Visits&edge_flat=false\n',
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JnyJny/busylight.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
