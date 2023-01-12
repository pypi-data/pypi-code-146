# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clockpuncher', 'clockpuncher.gui', 'clockpuncher.tests']

package_data = \
{'': ['*'], 'clockpuncher': ['data/*', 'fonts/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'dataset>=1.4.1,<2.0.0', 'dearpygui==0.6.415']

entry_points = \
{'console_scripts': ['clockpuncher = clockpuncher.main:main']}

setup_kwargs = {
    'name': 'clockpuncher',
    'version': '0.1.4',
    'description': 'A hackable GUI time tracker designed to be easily modified for user-centric automation.',
    'long_description': "# ClockPuncher\n\n## Abstract\n\nThis is a small python utility app that is being designed for time-tracking. As the name suggests, this is trying to replace track.toggl.com for tracking my own work.\n\nThe end-goal is a local, open-source timer that is hackable and can automate specific tasks like uploading/submitting billable hours.\n\n## Images\n### 'Production' GUI for usage\n![Productions View](repo_resources/clockpuncher.gif)\n### Development GUI with logger and debugger windows\n![Development View](./repo_resources/development_mode.png)\n\n## Installation\n\nThe best way is to use [pipx](https://pipxproject.github.io/pipx/) and run `pipx install clockpuncher` or `pipx run clockpuncher`.\n\nOn install a folder will be created in `~/.local/Clockpuncher` to contain local data storage. It should contain a sqlite db called `timer.db` and possibly wal files. It's literally just a sqlite database, you can access, query, and adjust as you would with any other database. This might be slightly different depending on your OS.\n\nYou can delete this folder without issue, but you will lose all your stored data.\n\n## Current Next Steps:\n* [X] Integrate sqlite DB of timer sessions\n* [X] Add inputs for specific task descriptions (text box)\n* [ ] Add on-the-fly graph representations\n  * [X] Task Breakdown\n  * [ ] Total Hours (per task and total)\n  * [ ] Total Billed (per task and total)\n* [ ] Add report CSV output\n* [ ] Add tests for main.py + gui module\n* [X] Put on PyPI\n* [X] Setup with pipx for app deployment\n* [ ] Add user settings with persistent storage\n* [ ] Add database back-up/cold-storage option\n\n## Repo Structure\n\nThis repo follows a pretty standard layout with `main.py` being the GUI front-end + database composed together to make the stopwatch app itself.\n\n\n### Outline:\n\n* `clockpuncher/`  - contains all code required to run Clock Puncher\n   * `main.py` - The main file that combines GUI, database, and application logic to make the above images\n   * `database.py` - Contains the Database class that does CRUD operations for main.py\n   * `models.py` - Dataclasses that represent rows in the Entries and Projects table\n   * `platform_local_storage.py` - Local storage location constants for \n   * `data/` - Contains local data storage. In production it stores data in `data/timer.db`\n   * `gui/` - All reusable GUI components\n     * `base_gui.py` - Base GUI class with loggers and basic development/production switchers.\n     * `dev_gui.py` - This holds quick GUI screens tossed together for development.\n     * `entry_visualization.py` - Contains task_chart and entry_table components and their class definitions\n      * `timer.py` - Contains Timer and Number GUI components that make up the clock display\n   * `tests` - Test suite using Pytest + Hypothesis\n\n",
    'author': 'Erin Maestas',
    'author_email': 'ErinLMaestas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
