# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kerykeion', 'kerykeion.aspects', 'kerykeion.charts', 'kerykeion.kr_types']

package_data = \
{'': ['*'], 'kerykeion.charts': ['templates/*']}

install_requires = \
['jsonpickle>=3.0.1,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyswisseph>=2.10.3.1,<3.0.0.0',
 'pytz>=2022.7,<2023.0',
 'requests-cache>=0.9.7,<0.10.0',
 'requests>=2.28.1,<3.0.0',
 'terminaltables>=3.1.10,<4.0.0']

entry_points = \
{'console_scripts': ['create-docs = scripts.docs:main']}

setup_kwargs = {
    'name': 'kerykeion',
    'version': '4.0a4',
    'description': 'A python library for astrology.',
    'long_description': '<h1 align=center>Kerykeion</h1>\n<div align="center">\n    <a href="#">\n        <img src="https://img.shields.io/github/contributors/g-battaglia/kerykeion?color=blue&logo=github" alt="contributors">\n    </a>\n    <a href="#">\n        <img src="https://img.shields.io/github/stars/g-battaglia/kerykeion.svg?logo=github" alt="stars">\n    </a>\n    <a href="#">\n        <img src="https://img.shields.io/github/forks/g-battaglia/kerykeion.svg?logo=github" alt="forks">\n    </a>\n    <a href="https://pypi.org/project/kerykeion" target="_blank">\n        <img src="https://visitor-badge.laobi.icu/badge?page_id=g-battaglia.kerykeion" alt="visitors"/>\n    </a>    \n    <a href="https://pypi.org/project/kerykeion" target="_blank">\n        <img src="https://img.shields.io/pypi/v/kerykeion?label=pypi%20package" alt="Package version">\n    </a>\n    <a href="https://pypi.org/project/kerykeion" target="_blank">\n        <img src="https://img.shields.io/pypi/pyversions/kerykeion.svg" alt="Supported Python versions">\n    </a>\n</div>\n\n&nbsp;\n\nKerykeion is a python library for Astrology.\nIt can calculate all the planet and house position,\nalso it can calculate the aspects of a single persone or between two, you can set how many planets you\nneed in the settings in the utility module.\nIt also can generate an SVG of a birthchart, a composite chart or a transit chart.\n\n## Installation\n\nKerykeion is a *Python 3.9* package, make sure you have *Python 3.9* or above installed on your system.\n\n```bash\npip3 install kerykeion\n```\n\n## Usage\n\nHere some examples:\n\n```python\n\n# Import the main class for creating a kerykeion instance:\nfrom kerykeion import KrInstance\n\n# Create a kerykeion instance:\n# Args: Name, year, month, day, hour, minuts, city, nation(optional)\nkanye = KrInstance("Kanye", 1977, 6, 8, 8, 45, "Atlanta")\n\n# Get the information about the sun in the chart:\n# (The position of the planets always starts at 0)\nkanye.sun\n\n#> {\'name\': \'Sun\', \'quality\': \'Mutable\', \'element\': \'Air\', \'sign\': \'Gem\', \'sign_num\': 2, \'pos\': 17.598992059774275, \'abs_pos\': 77.59899205977428, \'emoji\': \'♊️\', \'house\': \'12th House\', \'retrograde\': False}\n\n# Get informations about the first house:\nkanye.first_house\n\n#> {\'name\': \'First House\', \'quality\': \'Cardinal\', \'element\': \'Water\', \'sign\': \'Can\', \'sign_num\': 3, \'pos\': 17.995779673209114, \'abs_pos\': 107.99577967320911, \'emoji\': \'♋️\'}\n\n# Get element of the moon sign:\nkanye.moon.get("element")\n\n#> \'Water\'\n\n```\n\n**To avoid connecting to GeoNames (eg. avoiding hourly limit or no internet connection) you should instance kerykeion like this:**\n\n```python\nkanye = KrInstance(\n    "Kanye", 1977, 6, 8, 8, 45,\n    lng=50, lat=50, tz_str="Europe/Rome"\n    )\n```\n\n## Generate a SVG Chart:\n\n```python\nfrom kerykeion import KrInstance, MakeSvgInstance\n\nfirst = KrInstance("Jack", 1990, 6, 15, 15, 15, "Roma")\nsecond = KrInstance("Jane", 1991, 10, 25, 21, 00, "Roma")\n\n# Set the type, it can be Natal, Composite or Transit\n\nname = MakeSvgInstance(first, chart_type="Composite", second_obj=second)\nname.makeSVG()\nprint(len(name.aspects_list))\n\n#> Generating kerykeion object for Jack...\n#> Generating kerykeion object for Jane...\n#> Jack birth location: Roma, 41.89193, 12.51133\n#> SVG Generated Correctly\n#> 38\n\n```\n\n![alt text](http://centuryboy.altervista.org/JackComposite_Chart.svg)\n\n\n# Report\n\nTo print a report of all the data:\n\n```python\nfrom kerykeion import Report, KrInstance\n\nkanye = KrInstance("Kanye", 1977, 6, 8, 8, 45, "Atlanta")\nreport = Report(kanye)\nreport.print_report()\n\n```\n\nReturns:\n\n```\n+- Kerykeion report for Kanye -+\n+----------+------+-------------+-----------+----------+\n| Date     | Time | Location    | Longitude | Latitude |\n+----------+------+-------------+-----------+----------+\n| 8/6/1977 | 8:45 | Atlanta, US | -84.38798 | 33.749   |\n+----------+------+-------------+-----------+----------+\n+-----------+------+-------+------+----------------+\n| Planet    | Sign | Pos.  | Ret. | House          |\n+-----------+------+-------+------+----------------+\n| Sun       | Gem  | 17.6  | -    | Twelfth House  |\n| Moon      | Pis  | 16.43 | -    | Ninth House    |\n| Mercury   | Tau  | 26.29 | -    | Eleventh House |\n| Venus     | Tau  | 2.03  | -    | Tenth House    |\n| Mars      | Tau  | 1.79  | -    | Tenth House    |\n| Jupiter   | Gem  | 14.61 | -    | Eleventh House |\n| Saturn    | Leo  | 12.8  | -    | Second House   |\n| Uranus    | Sco  | 8.27  | R    | Fourth House   |\n| Neptune   | Sag  | 14.69 | R    | Fifth House    |\n| Pluto     | Lib  | 11.45 | R    | Fourth House   |\n| Mean_Node | Lib  | 21.49 | R    | Fourth House   |\n| True_Node | Lib  | 22.82 | R    | Fourth House   |\n+-----------+------+-------+------+----------------+\n+----------------+------+----------+\n| House          | Sign | Position |\n+----------------+------+----------+\n| First House    | Can  | 18.0     |\n| Second House   | Leo  | 9.51     |\n| Third House    | Vir  | 4.02     |\n| Fourth House   | Lib  | 3.98     |\n| Fifth House    | Sco  | 9.39     |\n| Sixth House    | Sag  | 15.68    |\n| Seventh House  | Cap  | 18.0     |\n| Eighth House   | Aqu  | 9.51     |\n| Ninth House    | Pis  | 4.02     |\n| Tenth House    | Ari  | 3.98     |\n| Eleventh House | Tau  | 9.39     |\n| Twelfth House  | Gem  | 15.68    |\n+----------------+------+----------+\n\n```\n\nAnd if you want to export it to a file:\n\n```bash\n$ python3 your_script_name.py > file.txt \n```\n\n## Other exeples of possibles usecase\n\n```python\n# Get all aspects between two persons:\n\nfrom kerykeion import CompositeAspects, KrInstance\nfirst = KrInstance("Jack", 1990, 6, 15, 15, 15, "Roma")\nsecond = KrInstance("Jane", 1991, 10, 25, 21, 00, "Roma")\n\nname = CompositeAspects(first, second)\naspect_list = name.get_relevant_aspects()\nprint(aspect_list[0])\n\n#> Generating kerykeion object for Jack...\n#> Generating kerykeion object for Jane...\n#> {\'p1_name\': \'Sun\', \'p1_abs_pos\': 84.17867971515636, \'p2_name\': \'Sun\', \'p2_abs_pos\': 211.90472999502984, \'aspect\': \'trine\', \'orbit\': 7.726050279873476, \'aspect_degrees\': 120, \'color\': \'#36d100\', \'aid\': 6, \'diff\': 127.72605027987348, \'p1\': 0, \'p2\': 0}\n\n```\n\n## Documentation\n\nMost of the functions and the classes are self documented by the types and have docstrings.\nAn auto-generated documentation [is available here](https://g-battaglia.github.io/kerykeion).\n\nSooner or later I\'ll try to write an extensive documentation.\n\n## Development\n\nYou can clone this repository or download a zip file using the right side buttons.\n\n## Contributing\n\nFeel free to contribute to the code!\n',
    'author': 'Giacomo Battaglia',
    'author_email': 'battaglia.giacomo@yahoo.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/g-battaglia/kerykeion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
