# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sightlines', 'sightlines.cell_functions']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.9.1.post1,<4.0.0',
 'launchpad-py>=0.9.1,<0.10.0',
 'pdpyras>=4.5.2,<5.0.0',
 'pygame>=2.1.2,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['sightlines-buildkite = apps.buildkite:main',
                     'sightlines-rainbow = apps.rainbow:main']}

setup_kwargs = {
    'name': 'sightlines',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Sightlines\n\nSightlines is a framework for using a [Novation Launchpad] as an information\ndisplay and control panel for general computing tasks.\n\nSightlines is made possible by the [`launchpad.py`] library, written by @FMMT666.\n\n## Quick Start\n\n- Install Sightlines:  `pip install git+ssh://git@github.com/jarpy/sightlines`\n- Run a sample app: `sightlines-rainbow`\n\n## Writing an App (WIP)\n\n### Cell\n\n\n\n### Grid\n\nIndividual cells are not much fun. The `Grid` class collect all the cells in the main 8x8 grid of the launchpad together. You can then look up cells in various ways.\n\n#### Linear Addressing\n\nAll the grid cells are available for lookup by linear index. They are numbered 0 to 63, starting top-left and proceeding left-to right, then top to bottom (revealing the cultural bias of the author).\n\n```python\ngrid = Grid()\ntop_left_cell = grid[0]\nbottom_right_cell = grid[63]\n```\n\n#### Cartesian Addressing\n\nYou can use x/y coordinates to get a cell in a more spatial way.\n\n```python\ngrid = Grid()\ntop_left_cell = grid[0, 0]\nbottom_right_cell = grid[7, 7]\n```\n\n#### Slicing\n\nFinally, you can use Python's slicing syntax.\n\n```python\ngrid = Grid()\nsecond_row = grid[8:15]\n```\n\n### CellRunner\n\nAs a rule, information displays periodically gather some data and then update the display output with what they learned. Sightlines encapsulates this behaviour in the `CellRunner` class. A `CellRunner` takes a collection of cells, and a function. It then periodically calls the function and does whatever is in it, generally setting the color of the cells.\n\n```python\ndef be_green(cells):\n    for cell in cells:\n        cell.set_rgb(0, 127, 0)\n\nCellRunner()\n```\n\n### Cell Functions\n\nWhen you press a cell on the Launchpad, it can do... stuff. \n\n[Novation Launchpad]: https://novationmusic.com/en/launch\n[`launchpad.py`]: https://github.com/FMMT666/launchpad.py\n",
    'author': 'Toby McLaughlin',
    'author_email': 'toby@jarpy.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
