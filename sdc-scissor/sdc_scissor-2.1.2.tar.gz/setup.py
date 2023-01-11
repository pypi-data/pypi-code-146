# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdc_scissor',
 'sdc_scissor.feature_extraction_api',
 'sdc_scissor.machine_learning_api',
 'sdc_scissor.obstacle_api',
 'sdc_scissor.sdc_prioritizer',
 'sdc_scissor.sdc_prioritizer.code.python',
 'sdc_scissor.sdc_prioritizer.datasets.fullroad.BeamNG_AI.BeamNG_RF_1_5',
 'sdc_scissor.sdc_prioritizer.testPrioritization',
 'sdc_scissor.sdc_prioritizer.testPrioritization.crossover',
 'sdc_scissor.sdc_prioritizer.testPrioritization.mutation',
 'sdc_scissor.sdc_prioritizer.testPrioritization.problem',
 'sdc_scissor.simulator_api',
 'sdc_scissor.testing_api',
 'sdc_scissor.testing_api.test_generators.ambiegen',
 'sdc_scissor.testing_api.test_generators.ambiegen.Utils',
 'sdc_scissor.testing_api.test_generators.frenetic',
 'sdc_scissor.testing_api.test_generators.frenetic.src',
 'sdc_scissor.testing_api.test_generators.frenetic.src.generators',
 'sdc_scissor.testing_api.test_generators.frenetic.src.utils',
 'sdc_scissor.testing_api.test_generators.frenetic_v',
 'sdc_scissor.testing_api.test_generators.frenetic_v.src',
 'sdc_scissor.testing_api.test_generators.frenetic_v.src.generators',
 'sdc_scissor.testing_api.test_generators.frenetic_v.src.utils']

package_data = \
{'': ['*'],
 'sdc_scissor.sdc_prioritizer': ['code/*',
                                 'code/r-script/*',
                                 'datasets/fullroad/*',
                                 'datasets/fullroad/BeamNG_AI/*',
                                 'datasets/fullroad/BeamNG_AI/BeamNG_RF_1/*',
                                 'datasets/fullroad/BeamNG_AI/BeamNG_RF_2/*',
                                 'datasets/fullroad/Driver_AI/*',
                                 'docker_scripts/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Shapely>=1.8.1,<2.0.0',
 'beamngpy==1.22',
 'click>=8.0.4,<9.0.0',
 'icontract>=2.6.2,<3.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pymoo==0.4.2.2',
 'scikit-learn>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['sdc-scissor = sdc_scissor.cli:cli']}

setup_kwargs = {
    'name': 'sdc-scissor',
    'version': '2.1.2',
    'description': 'A cost-effective test selection for self-driving cars in virtual environments',
    'long_description': '# SDC-Scissor\n```{code-block} text\n ____    ____    ____              ____                                                \n/\\  _`\\ /\\  _`\\ /\\  _`\\           /\\  _`\\           __                                 \n\\ \\,\\L\\_\\ \\ \\/\\ \\ \\ \\/\\_\\         \\ \\,\\L\\_\\    ___ /\\_\\    ____    ____    ___   _ __  \n \\/_\\__ \\\\ \\ \\ \\ \\ \\ \\/_/_  _______\\/_\\__ \\   /\'___\\/\\ \\  /\',__\\  /\',__\\  / __`\\/\\`\'__\\\n   /\\ \\L\\ \\ \\ \\_\\ \\ \\ \\L\\ \\/\\______\\ /\\ \\L\\ \\/\\ \\__/\\ \\ \\/\\__, `\\/\\__, `\\/\\ \\L\\ \\ \\ \\/ \n   \\ `\\____\\ \\____/\\ \\____/\\/______/ \\ `\\____\\ \\____\\\\ \\_\\/\\____/\\/\\____/\\ \\____/\\ \\_\\ \n    \\/_____/\\/___/  \\/___/            \\/_____/\\/____/ \\/_/\\/___/  \\/___/  \\/___/  \\/_/ \n                                                                                       \n                                                                                       \n```\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)\n[![GitHub issues](https://img.shields.io/github/issues/ChristianBirchler/sdc-scissor)](https://github.com/ChristianBirchler/sdc-scissor/issues)\n[![GitHub forks](https://img.shields.io/github/forks/ChristianBirchler/sdc-scissor)](https://github.com/ChristianBirchler/sdc-scissor/network)\n[![GitHub stars](https://img.shields.io/github/stars/ChristianBirchler/sdc-scissor)](https://github.com/ChristianBirchler/sdc-scissor/stargazers)\n[![](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/ci.yml/badge.svg)](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/ci.yml)\n[![CD](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/cd.yml/badge.svg)](https://github.com/ChristianBirchler/sdc-scissor/actions/workflows/cd.yml)\n[![PyPI](https://img.shields.io/pypi/v/sdc-scissor)](https://pypi.org/project/sdc-scissor/)\n[![](https://readthedocs.org/projects/sdc-scissor/badge)](https://sdc-scissor.readthedocs.io)\n[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=alert_status)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=ncloc)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=coverage)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=sqale_index)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=reliability_rating)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=duplicated_lines_density)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=vulnerabilities)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=bugs)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=security_rating)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=sqale_rating)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![](https://sonarcloud.io/api/project_badges/measure?project=ChristianBirchler_sdc-scissor&metric=code_smells)](https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor)\n[![DOI](https://zenodo.org/badge/363107094.svg)](https://zenodo.org/badge/latestdoi/363107094)\n<div style="text-align: center;">\n<a href="https://github.com/ChristianBirchler/sdc-scissor">\n<img src="https://raw.githubusercontent.com/ChristianBirchler/sdc-scissor/main/docs/images/github_logo_icon.png">\n</a>\n<a href="https://sonarcloud.io/summary/overall?id=ChristianBirchler_sdc-scissor">\n<img src="https://sonarcloud.io/images/project_badges/sonarcloud-black.svg">\n</a>\n</div>\n\n## A Tool for Cost-effective Simulation-based Test Selection in Self-driving Cars Software\nSDC-Scissor is a tool that let you test self-driving cars more efficiently in simulation. It uses a machine-learning\napproach to select only relevant test scenarios so that the testing process is faster. Furthermore, the selected tests\nare diverse and try to challenge the car with corner cases.\n\nFurthermore, this repository contains also code for test multi-objective test case prioritization with an evolutionary\ngenetic search algorithm. If you are interested in prioritizing test cases, then you should read the dedicated\n[README.md](https://github.com/ChristianBirchler/sdc-scissor/blob/main/sdc_scissor/sdc_prioritizer/testPrioritization/README.md)\nfor this. If you use the prioritization technique then also cite the papers from the reference section!\n\n## Support\nWe use [GitHub Discussions](https://github.com/ChristianBirchler/sdc-scissor/discussions) as a community platform. You\ncan ask questions and get support there from the community. Furthermore, new features and releases will be discussed and\nannounced there.\n\n## Documentation\nFor the documentation follow the link: [sdc-scissor.readthedocs.io](https://sdc-scissor.readthedocs.io/en/latest/)\n\n[![](https://raw.githubusercontent.com/ChristianBirchler/sdc-scissor/main/docs/images/readthedocs.png)](https://sdc-scissor.readthedocs.io/en/latest/)\n\n## License\n```{code-block} text\nSDC-Scissor tool for cost-effective simulation-based test selection\nin self-driving cars software.\nCopyright (C) 2022  Christian Birchler\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n```\n\nThe software we developed is distributed under GNU GPL license. See the\n[LICENSE.md](https://github.com/ChristianBirchler/sdc-scissor/blob/main/LICENSE.md) file.\n\n## References\nIf you use this tool in your research, please cite the following papers:\n\n- **Christian Birchler**, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella, "Cost-effective Simulation-based Test Selection in Self-driving Cars Software with SDC-Scissor," *In 2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)*, pp. 164-168, doi: 10.1109/SANER53432.2022.00030.\n  - [IEEE Xplore](https://doi.org/10.1109/SANER53432.2022.00030)\n  - [Preprint](https://doi.org/10.21256/zhaw-24017)\n  - [GitHub](https://github.com/ChristianBirchler/sdc-scissor)\n````{code-block} bibtex\n@inproceedings{Birchler2022Cost1,\n  author={Birchler, Christian and Ganz, Nicolas and Khatiri, Sajad and Gambi, Alessio, and Panichella, Sebastiano},\n  booktitle={2022 IEEE 29th International Conference on Software Analysis, Evolution and Reengineering (SANER)},\n  title={Cost-effective Simulationbased Test Selection in Self-driving Cars Software with SDC-Scissor},\n  year={2022},\n  doi={10.1109/SANER53432.2022.00030}\n}\n````\n- **Christian Birchler**, Nicolas Ganz, Sajad Khatiri, Alessio Gambi, and Sebastiano Panichella, "Cost-effective Simulation-based Test Selection in Self-driving Cars Software," *Science of Computer Programming (SCP)*, doi: to appear, 2022.\n  - [Accepted manuscript version](https://doi.org/10.48550/arXiv.2211.11409)\n````{code-block} bibtex\n@article{Birchler2022Cost2,\n  author    = {Christian Birchler and Nicolas Ganz and Sajad Khatiri and Alessio Gambi and Sebastiano Panichella},\n  title     = {Cost-effective Simulation-based Test Selection in Self-driving Cars Software},\n  journal   = {Science of Computer Programming (SCP)},\n  year      = {2022},\n  doi       = {to appear},\n  eprinttype = {arXiv},\n  eprint    = {2211.11409}\n}\n````\n- **Christian Birchler**, Sajad Khatiri, Bill Bosshard, Alessio Gambi, and Sebastiano Panichella, "Machine Learning-based Test Selection for Simulation-based Testing of Self-driving Cars Software," *Empirical Software Engineering (EMSE)*, doi: to appear, 2022.\n  - [Preprint](https://doi.org/10.48550/arXiv.2212.04769)\n````{code-block} bibtex\n@article{Birchler2022Machine,\n  author    = {Christian Birchler and Sajad Khatiri and Bill Bosshard and Alessio Gambi and Sebastiano Panichella},\n  title     = {Machine Learning-based Test Selection for Simulation-based Testing of Self-driving Cars Software},\n  journal   = {Empirical Software Engineering (EMSE)},\n  year      = {2022},\n  doi       = {to appear},\n  eprinttype = {arXiv},\n  eprint    = {2212.04769}\n}\n````\n- **Christian Birchler**, Sajad Khatiri, Pouria Derakhshanfar, Sebastiano Panichella, and Annibale Panichella, "Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments," *ACM Transactions on Software Engineering and Methodology (TOSEM)*, doi: 10.1145/3533818, 2022.\n  - [ACM Digital Library](https://doi.org/10.1145/3533818)\n  - [Preprint](https://doi.org/10.48550/arXiv.2107.09614)\n```{code-block} bibtex\n@article{Birchler2022Single,\n  author={Birchler, Christian and Khatiri, Sajad and Derakhshanfar, Pouria and Panichella, Sebastiano and Panichella, Annibale},\n  title={Single and Multi-objective Test Cases Prioritization for Self-driving Cars in Virtual Environments},\n  year={2022},\n  publisher={Association for Computing Machinery},\n  journal={ACM Transactions on Software Engineering and Methodology (TOSEM)},\n  doi={10.1145/3533818}\n}\n```\n\n## Contacts\n* Christian Birchler\n    * Zurich University of Applied Science (ZHAW), Switzerland - birc@zhaw.ch\n* Nicolas Ganz\n    * Zurich University of Applied Science (ZHAW), Switzerland - gann@zhaw.ch\n* Sajad Khatiri\n    * Zurich University of Applied Science (ZHAW), Switzerland - mazr@zhaw.ch\n* Dr. Alessio Gambi\n    * Passau University, Germany - alessio.gambi@uni-passau.de\n* Dr. Sebastiano Panichella\n    * Zurich University of Applied Science (ZHAW), Switzerland - panc@zhaw.ch\n',
    'author': 'Christian Birchler',
    'author_email': 'birchler.chr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ChristianBirchler/sdc-scissor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
