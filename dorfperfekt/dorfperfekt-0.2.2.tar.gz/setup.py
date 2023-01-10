# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dorfperfekt']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.2.3,<7.0.0',
 'aenum>=3.1.8,<4.0.0',
 'cachetools>=5.0.0,<6.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0']

entry_points = \
{'console_scripts': ['dorfperfekt = dorfperfekt.__main__:main']}

setup_kwargs = {
    'name': 'dorfperfekt',
    'version': '0.2.2',
    'description': 'Tile placement suggestions for the game Dorfromantik.',
    'long_description': '# Dorfperfekt\n\nTile placement suggestions for the game Dorfromantik. With an emphasis on perfect tile placement, this software tool enables the player to play indefinitely (and achieve a massive score while doing so).\n\n![demo dorfperfekt](https://github.com/amosborne/dorfperfekt/raw/main/demo_dorfperfekt.png)\n![demo dorfromantik map](https://github.com/amosborne/dorfperfekt/raw/main/demo_dorfromantik_map.png)\n![demo dorfromantik score](https://github.com/amosborne/dorfperfekt/raw/main/demo_dorfromantik_score.png)\n\n## How It Works\n\nThe player inputs a six-character text string representing the next tile to be placed. Each valid placement is then evaluated by the solver according to the following (in order of precedence):\n\n1. How many tiles would be ruined by this placement? Less is better.\n2. Of the tiles encountered so far, how many would alternatively fit perfectly at this position? Less is better.\n3. Assuming this placement is made, consider each adjacent open position. Of the tiles encountered so far, how many would fit perfectly at that adjacent position? Take the minimum of all adjacent open positions. More is better.\n\nThe latter two computations will take a significant amount of time as the game progresses and more unique tiles are encountered. A threshold is set by the user so that the solver can be instructed to ignore rarer tiles.\n\n## Using the Application\n\nDorfperfekt displays an overall map of the board. Dark gray tiles are non-ruined placements and light gray tiles are ruined placements. After entering a tile definition string and pressing the solve button, the progress bar will increment and pressing the refresh button will overlay a heatmap of the possible moves onto the board. Green is better, red is worse, and white is neutral (or not yet evaluated).\n\nPositions on the map can be clicked on. By clicking on a proposed position for your next placement, a view of the local terrain is generated. The tile to be placed is given a proposed best rotation but the user may use the rotate button to select an alternate rotation.\n\nExisting tiles may also be clicked on such that they may be deleted or set as the origin to recenter the map of the board.\n\n## Tile Definitions\n\nA tile is defined by a six-character text string where each character represents the edge terrains in **clockwise** order. If all edges of the tile are the same a single character may be used instead. Tile characters are deliberately selected to all be accessible from the left hand.\n\n- Grass, "g"\n- Forest, "f"\n- Ranch, "r" (ie. wheat/lavender fields)\n- Dwelling, "d" (ie. houses)\n- Water, "w" (ie. rivers)\n- Station, "s"\n- Train, "t"\n- Coast, "c" (ie. lakes)\n\n## Installation\n\nFrom the command line, install with `pip install dorfperfekt`. The application can then be run from the command line with `dorfperfekt`.\n\n## Development\n\nSetting up the software development environment is easy.\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n',
    'author': 'amosborne',
    'author_email': 'amosborne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/amosborne/dorfperfekt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
