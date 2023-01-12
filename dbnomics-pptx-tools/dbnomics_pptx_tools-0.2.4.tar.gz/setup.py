# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbnomics_pptx_tools', 'dbnomics_pptx_tools.charts']

package_data = \
{'': ['*']}

install_requires = \
['DBnomics>=1.2.3,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'daiquiri>=3.2.1,<4.0.0',
 'lxml>=4.9.1,<5.0.0',
 'parsy>=2.0,<3.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-pptx>=0.6.21,<0.7.0',
 'python-slugify>=7.0.0,<8.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['dbnomics-pptx = dbnomics_pptx_tools.cli:app']}

setup_kwargs = {
    'name': 'dbnomics-pptx-tools',
    'version': '0.2.4',
    'description': 'DBnomics PowerPoint (pptx) tools',
    'long_description': '# DBnomics PowerPoint (pptx) tools\n\nThis CLI tool allows to update data coming from DBnomics in PowerPoint presentations.\n\n## Usage\n\nFirst, define a YAML metadata file describing the charts and tables on each slide to update.\n\nFor example see [simple_presentation_1.yaml](./samples/simple_presentation_1.yaml).\n\nSee the [metadata file](#metadata-file) section below for more details.\n\nThe `dbnomics-pptx` CLI command provides 2 commands: `fetch` and `update`.\n\n### `fetch` command\n\nThis command reads all the series needed by the charts and tables of all slides in the YAML metadata file, deduplicate and download them in a cache directory, where they are stored as JSON files.\n\n```bash\ndbnomics-pptx fetch samples/simple_presentation_1.yaml\n```\n\nUse the `-v` option to display debug messages.\n\nBy default, the series that are already present in the cache directory are skipped, in order to avoid putting pressure on DBnomics servers.\nUse the `--force` option to always download them.\n\n### `update` command\n\nThis command takes a PowerPoint presentation file in input, and a YAML metadata file, and updates the charts and tables defined in the metadata file, then saves the result in an output presentation file (it does not modify the input one).\n\n```bash\ndbnomics-pptx update samples/simple_presentation_1.pptx --metadata-file samples/simple_presentation_1.yaml samples/simple_presentation_1.output.pptx\n```\n\nUse the `-v` option to display debug messages.\n\n## Metadata file\n\n```yaml\nslides:\n  My slide 1: # the title of the slide\n    charts:\n      My chart 1: # the name of the chart (as defined in the "Selection pane")\n        series:\n          - OECD/GDP_GROWTH/W.USA.tracker_yoy # simple form: the series ID\n          - id: OECD/GDP_GROWTH/W.Eurozone.tracker_yoy # extended form: a map of the ID and the name of the series\n            name: Eurozone\n    tables:\n      My table 1: # the name of the table (as defined in the "Selection pane")\n        series:\n          - OECD/KEI/NAEXKP01.EA19.GP.A\n          - OECD/KEI/NAEXKP01.DEU.GP.A\n          - OECD/KEI/NAEXKP01.FRA.GP.A\n          - OECD/KEI/NAEXKP01.ITA.GP.A\nseries: # a map of properties for series, shared between all the charts and tables of all slides\n  OECD/GDP_GROWTH/W.USA.tracker_yoy:\n    name: United States\n  OECD/KEI/NAEXKP01.DEU.GP.A:\n    name: Germany\n  OECD/KEI/NAEXKP01.EA19.GP.A:\n    name: Euro Area\n  OECD/KEI/NAEXKP01.FRA.GP.A:\n    name: France\n  OECD/KEI/NAEXKP01.ITA.GP.A:\n    name: Italy\n```\n\nSeries properties defined in charts of tables have a higher precedence level than the ones defines in the top-level `series` map (which act as a fallback).\n\nFor example, here the name of the series `OECD/GDP_GROWTH/W.Eurozone.tracker_yoy` is defined at the chart level, in "My chart 1" (the name is "Eurozone"), and it is not defined in the top-level `series` map.\nOn the contrary, in "My chart 1", the named of the series `OECD/GDP_GROWTH/W.USA.tracker_yoy` is not defined, and will be found in the top-level `series` map, where it is defined as "United States".\n\n### How to know the names of the charts/tables?\n\nThe names of the charts and tables can be read or modified in the "Selection pane" in PowerPoint.\n\nThe "Selection pane" can be opened with Alt+F10 in PowerPoint.\nThen you just have to select a chart or a table, and it will highlight the corresponding line in the "Selection pane", showing its name.\n\nYou can also modify the name to improve readability.\n\nOnce you get the name of a chart or a table, you can put it in the YAML file.\nIn the previous example, the names are "My chart 1" and "My table 1".\n\nSee also:\n\n- [Manage objects with the Selection pane](https://support.microsoft.com/en-us/office/manage-objects-with-the-selection-pane-a6b2fd3e-d769-46c1-9b9c-b94e04a72550)\n- [The PowerPoint Selection Pane](https://www.presentationpoint.com/blog/powerpoint-selection-pane/)\n',
    'author': 'Christophe Benz',
    'author_email': 'christophe.benz@nomics.world',
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
