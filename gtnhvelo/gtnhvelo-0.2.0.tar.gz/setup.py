# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gtnhvelo',
 'gtnhvelo.data',
 'gtnhvelo.graph',
 'gtnhvelo.gtnh',
 'gtnhvelo.module',
 'gtnhvelo.prototypes']

package_data = \
{'': ['*'], 'gtnhvelo': ['resources/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'graphviz>=0.20.1,<0.21.0',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'rich>=13.0.0,<14.0.0',
 'sympy>=1.11.1,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['flow = gtnhvelo.cli:main']}

setup_kwargs = {
    'name': 'gtnhvelo',
    'version': '0.2.0',
    'description': 'Factory Optimization Flowcharts for Gregtech: New Horizons',
    'long_description': '<h1>gtnh-velo <img src="https://img.shields.io/github/license/velolib/gtnh-velo?style=flat-square"/> </h1>\n<!-- TODO: Shorten the readme to move some of it into the wiki -->\n\n## ❓ What is it?\n\nThis is a fork of OrderedSet86\'s [gtnh-flow](https://github.com/OrderedSet86/gtnh-flow). In addition to the functionalities of the original tool, this fork has:\n1. Extended formatting of projects\n2. Added stylization add formatting of graphs\n3. Standards to increase readability\n4. A custom CLI\n\n## 📖 Samples\nSamples of the graphs in the repository.\n<details open>\n    <summary><strong>Samples</strong></summary>\n    <img src="samples/rutile-titanium.svg" alt="Rutile -> Titanium">\n    <img src="samples/epoxid.svg" alt="Epoxid">\n</details>\n\n## ⏲️ Installation\n### Install as Python package\nThis is the easiest installation method. In the terminal run:\n```\npip install gtnhvelo -U\n```\n\n\n### Linux\n1. Clone this repository `git clone https://github.com/velolib/gtnh-velo.git`\n2. Download Python 3 and install from `https://www.python.org/downloads/`\n3. Navigate to the cloned repository and install the required project dependencies `pip install -r requirements.txt`\n4. Install Graphviz, on Debian-based Linux it\'s `sudo apt-get install graphviz`\n    - If Graphviz is not added to the system path, you can add the path to the `/bin` folder in the configuration file.\n\n### Windows\n1. Clone this repository `git clone https://github.com/velolib/gtnh-velo.git`\n2. Download Python 3 and install from `https://www.python.org/downloads/`\n3. Navigate to the cloned repository and install the required project dependencies `pip install -r requirements.txt`\n4. Install Graphviz, for Windows there is a guide [here](https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224). Graphviz must be added to the system PATH for all users or the current user which may or may not need a system restart.\n    - If Graphviz is not added to the system path, you can add the path to the `/bin` folder in the configuration file.\n\n>It\'s recommended to create a virtual environment before installing to isolate the development environment from the global scope.\n\n\n## ⏲️ Usage\n### CLI\n1. Create a project under `projects/`. You can look at existing projects to see the structure.\n2. The project name is a system file path relative to `projects/`, for example `plastics/epoxid`. You can run the graph creator in 2 ways:\n    - `flow [project name]`\n    - `flow` then inputting your project name in the dialog\n3. The output graph will pop up and be available in `output/`\n\nWhen running `flow` the directories `projects/` and `output/` will be created in the working directory if they do not exist already.\n### In code\nYou can use gtnh-velo in Python code like this:\n```python\nfrom gtnhvelo import flow\nflow(\'project_name\', \'output_path\', \'projects_path\')\n```\nUsing gtnh-velo in Python also automatically turns on quiet mode.\n\n## ⁉ Answers\n### How to configure\nThe configuration file `config_factory_graph.yaml` will be created on startup in the working directory if not created already.\nYou can configure a variety of layout and functional options using it. Make sure to not delete any keys.\n\n### Automatic overclocking\nAll of the names in the following image are recognized and will be overclocked automatically to 1A of the tier you select. This includes the EBF, which will default to 1 hatch of the selected tier.\n<details>\n    <summary><strong>Recognized Overclocks</strong></summary>\n    <img src="https://github.com/OrderedSet86/gtnh-flow/raw/master/samples/recognized_ocs.png" alt="Recognized overclocks">\n</details>\n\n### Dealing with multi-I/O\nSometimes the balancing algorithm will fail. You may need to manually make the adjustments by renaming the ingredients so that it will only be used for the recipes you want. An example: `chlorine 1`, `chlorine 2`\n### Project Standards\nThis section will cover how to create a basic project.\n\n#### Basic recipes\nHere is how to write a recipe (note the indentation):\n```yaml\n- m: large chemical reactor\n  tier: HV # The recipe tier, minimum LV\n  I: # Inputs\n    nonrecycle hydrochloric acid: 3000\n    hydrochloric acid: 27000\n    raw silicon dust: 10\n  O: # Outputs\n    trichlorosilane: 9000\n    silicon tetrachloride: 300\n    hexachlorodisilane: 200\n    dichlorosilane: 300\n    \'[recycle] hydrogen\': 20400 # Recycle this output\n  eut: 480 # EU/t of recipe\n  dur: 7.5 # Recipe duration in seconds\n  group: silicon # Used to group recipes on the graph\n```\nIn every project there needs to be 1 (and only 1) recipe that needs to be locked. This is the recipe that every other recipe will be balanced off of. Here are the fields you need to add:\n```yaml\n# These 2 fields (target and number) are mutually exclusive!\n- m: example machine\n  target: # lock it to the number of a specific ingredient output per second\n    trichlorosilane: 4000\n# -------------------------------------------------------------------\n  number: 2 # lock the number of machines for this recipe\n```\n#### Advanced recipes\nThis section will cover the exceptions to the recipes.\nSome fields you need to know about:\n``` yaml\n- m: example machine\n  heat: 4001 # The required heat for a recipe\n  coils: nichrome # The selected coils for a recipe\n  saw_type: saw # The saw type for a Tree Growth Simulator\n  material: shadow # Turbine material for turbines\n  size: large # Turbine size for turbines\n  pipe_casings: tungstensteel # Pipe casings for chemplants\n```\n\n<details>\n    <summary><strong>Special Recipes</strong></summary>\n\n```yaml\n# Electric Blast Furnace example\n- m: electric blast furance\ntier: HV\nI:\n    tungstic acid: 7\nO:\n    tungsten trioxide: 4\neut: 480\ndur: 10\nheat: 1200\ncoils: nichrome\nnumber: 1\n```\n\n```yaml\n# Chemical Plant example\n- m: chem plant\ntier: LuV\nI:\n    pine wood: 0.1\nO:\n    crushed pine materials: 40\neut: 120\ndur: 10\ncoils: tungstensteel\npipe_casings: tungstensteel\n\n```\n\n```yaml\n# GT++ Machine example\n- m: industrial sifter\ntier: HV\nI:\n    platinum salt dust: 1\nO:\n    refined platinum salt dust: 0.95\neut: 30\ndur: 30\ngroup: pmp recycling\n\n```\n\n```yaml\n# Multiblock turbine example\n# in the finished graph it will calculate the actual numbers\n- m: LGT\ntier: EV\nI:\n    benzene: 1\nO: {}\neut: 0\ndur: 0\nmaterial: shadow\nsize: large\n```\n\n</details>\n\n\n\n## 🙏 Thanks\nVisit the original [gtnh-flow by OrderedSet](https://github.com/OrderedSet86/gtnh-flow). Without it this fork would not exist!\n\n',
    'author': 'velolib',
    'author_email': 'vlocitize@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
