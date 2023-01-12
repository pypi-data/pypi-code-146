# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ccs_fit',
 'ccs_fit.ase_calculator',
 'ccs_fit.common',
 'ccs_fit.common.math',
 'ccs_fit.data',
 'ccs_fit.debugging_tools',
 'ccs_fit.fitting',
 'ccs_fit.ppmd_interface',
 'ccs_fit.regression_tool',
 'ccs_fit.scripts']

package_data = \
{'': ['*']}

install_requires = \
['art>=5.8,<6.0',
 'ase>=3.22.1',
 'cvxopt>=1.3.0',
 'numpy>=1.22.4,<1.23.0',
 'pandas>=1.5.0',
 'pymatgen>=2023.1.9,<2024.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.9.2',
 'sympy>=1.11.1',
 'tqdm>=4.64.1']

setup_kwargs = {
    'name': 'ccs-fit',
    'version': '0.11.10',
    'description': 'Fitting tools for repulsive two body interactions using curvature constrained splines.',
    'long_description': '# CCS - Curvature Constrained Splines  \n\n[![Latest Release](https://img.shields.io/github/v/release/teoroo-cmc/ccs?display_name=tag&color=brightgreen&sort=semver)](https://github.com/Teoroo-CMC/CCS/releases/latest)\n[![License](https://img.shields.io/github/license/teoroo-cmc/ccs)](https://opensource.org/licenses/LGPL-3.0)\n[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.cpc.2020.107602-blue)](https://doi.org/10.1016/j.cpc.2020.107602)\n[![Build](https://img.shields.io/github/actions/workflow/status/teoroo-cmc/CCS/ci-cd.yml)](https://github.com/Teoroo-CMC/CCS/actions)\n\n<!--- [![Build Status](https://github.com/tblite/tblite/workflows/CI/badge.svg)](https://github.com/tblite/tblite/actions)\n[![Documentation](https://img.shields.io/badge/Github%20Pages-Pages-blue)](https://teoroo-cmc.github.io/CCS/)\n[![codecov](https://codecov.io/gh/tblite/tblite/branch/main/graph/badge.svg?token=JXIE6myqNH)](https://codecov.io/gh/tblite/tblite) \n[![Coverage](codecov.io/gh/:vcsName/:user/:repo?flag=flag_name&token=a1b2c3d4e5)(https://github.com/Teoroo-CMC/CCS/actions)\n--->\n\nThe `CCS` package is a tool to construct two-body potentials using the idea of curvature constrained splines.\n## Getting Started\n### Package Layout\n\n```\nccs-x.y.z\n├── CHANGELOG.md\n├── LICENSE\n├── MANIFEST.in\n├── README.md\n├── bin\n│\xa0\xa0 ├── ccs_build_db\n│\xa0\xa0 ├── ccs_export_sktable\n│\xa0\xa0 ├── ccs_fetch\n│\xa0\xa0 ├── ccs_fit\n│\xa0\xa0 └── ccs_validate\n├── docs\n├── examples\n│\xa0\xa0 ├── CCS\n│\xa0\xa0 ├── CCS_with_LAMMPS\n│\xa0\xa0 ├── DFTB_repulsive_fitting\n│\xa0\xa0 ├── Preparing_ASE_db_trainingsets\n│\xa0\xa0 ├── Simple_regressor\n│\xa0\xa0 ├── Twobody_fit_for_an_O2_molecule\n│\xa0\xa0 ├── Twobody_fit_for_solid_Ne\n│\xa0\xa0 └── ppmd_interfacing\n├── logo.png\n├── poetry.lock\n├── pyproject.toml\n├── src\n│\xa0\xa0 └── ccs\n│\xa0\xa0     ├── ase_calculator\n│\xa0\xa0     ├── common\n│\xa0\xa0     ├── data\n│\xa0\xa0     ├── debugging_tools\n│\xa0\xa0     ├── fitting\n│\xa0\xa0     ├── ppmd_interface\n│\xa0\xa0     ├── regression_tool\n│\xa0\xa0     └── scripts\n│\xa0\xa0         ├── ccs_build_db.py\n│\xa0\xa0         ├── ccs_export_sktable.py\n│\xa0\xa0         ├── ccs_fetch.py\n│\xa0\xa0         ├── ccs_fit.py\n│\xa0\xa0         └── ccs_validate.py\n└── tests\n```\n\n* `ccs_fetch`           - Executable to construct the traning-set (structures.json) from a pre-existing ASE-database with DFT-data.\n* `ccs_fit`             - The primary executable file for the ccs package.\n* `main.py`             - A module to parse input files.\n* `objective.py`        - A module which contains the objective function and solver.\n* `spline_functions.py` - A module for spline construction/evaluation/output. \n\n<!---\n### Prerequisites\n\nYou need to install the following softwares\n\n```\npip install numpy\npip install scipy\npip install ase\npip install cvxopt\n```\n### Installing from source\n\n#### Git clone\n\n```\ngit clone git@github.com/Teoroo-CMC/CCS.git\ncd CCS\npython setup.py install\n```\n--->\n### Installing from source using poetry\n```\ngit clone https://github.com/Teoroo-CMC/CCS_fit.git ccs_fit\ncd ccs_fit\n\n# Install python package manager poetry (see https://python-poetry.org/docs/ for more explicit installation instructions)\ncurl -sSL https://install.python-poetry.org | python3 -\n# You might have to add poetry to your PATH\npoetry --version # to see if poetry installed correctly\npoetry install # to install ccs_fit\n```\n### Environment Variables\nSet the following environment variables:\n```\n$export PYTHONPATH=<path-to-CCS-package>:$PYTHONPATH\n$export PATH=<path-to-CCS-bin>:$PATH\n\nWithin a conda virtual environment, you can update the path by using:\nconda develop <path-to-CCS-package>\n```\n\n\n## Tutorials\n\nWe provide tutorials in the [examples](examples/) folder. To run the example, go to one of the folders. Each contain the neccesery input files required for the task at hand. A sample `CCS_input.json` for O2 is shown below:\n```\n{\n        "General": {\n                "interface": "CCS"\n        },\n        "Train-set": "structures.json",\n        "Twobody": {\n                "O-O": {\n                        "Rcut": 2.5,\n                        "Resolution": 0.02,\n                        "Swtype": "sw"\n                }\n        },\n        "Onebody": [\n                "O"\n        ]\n}\n\n```\nThe `CCS_input.json` file should provide at a minimum the block "Genaral" specifying an interface. The default is to look for input structures in the file `structure.json` file. The format for `structure.json` is shown below :\n```\n{\n"energies":{\n        "S1": {\n                "Energy": -4.22425752,\n                "Atoms": {\n                        "O": 2\n                },\n                "O-O": [\n                        0.96\n                ]\n        },\n        "S2": {\n                "Energy": -5.29665634,\n                "Atoms": {\n                        "O": 2\n                },\n                "O-O": [\n                        0.98\n                ]\n        },\n        "S3": {\n                "Energy": -6.20910363,\n                "Atoms": {\n                        "O": 2\n                },\n                "O-O": [\n                        1.0\n                ]\n        },\n        "S4": {\n                "Energy": -6.98075271,\n                "Atoms": {\n                        "O": 2\n                },\n                "O-O": [\n                        1.02\n                ]\n        }\n}\n}\n```\nThe `structure.json` file contains different configurations labeled ("S1", "S2"...) and corresponding energy, pairwise distances (contained in an array labelled as "O-O" for oxygen). The stoichiometry of each configuration is given under the atoms label ("Atoms") as a key-value pair ("O" : 2 ). \n\n\nTo perform the fit : \n```\nccs_fit\n```\nThe following output files are obtained:\n```\nCCS_params.json CCS_error.out ccs.log \n```\n* CCS_params.json  - Contains the spline coefficients, and one-body terms for two body potentials.\n* error.out        - Contains target energies, predicted energies and absolute error for each configuration.\n* ccs.log          - Contains debug information\n## Authors\n\n* **Akshay Krishna AK** \n* **Jolla Kullgren** \n* **Eddie Wadbro** \n* **Peter Broqvist**\n* **Thijs Smolders**\n\n## Funding\nThis project has received funding from the European Union\'s Horizon 2020 research and innovation programme under grant agreement No 957189.\n\n## License\nThis project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.\n\n## Acknowledgement\nWe thank all the members of  [TEOROO-group](http://www.teoroo.kemi.uu.se/) at Uppsala University, Sweden.\n',
    'author': 'Akshay Krishna AK',
    'author_email': 'None',
    'maintainer': 'Jolla Kullgren',
    'maintainer_email': 'jolla.kullgren@kemi.uu.se',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
