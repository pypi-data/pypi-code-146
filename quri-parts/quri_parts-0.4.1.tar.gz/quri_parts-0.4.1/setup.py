# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quri_parts']

package_data = \
{'': ['*']}

install_requires = \
['quri-parts-algo', 'quri-parts-chem', 'quri-parts-circuit', 'quri-parts-core']

extras_require = \
{'braket': ['quri-parts-braket'],
 'cirq': ['quri-parts-cirq'],
 'openfermion': ['quri-parts-openfermion'],
 'qiskit': ['quri-parts-qiskit'],
 'qulacs': ['quri-parts-qulacs'],
 'stim': ['quri-parts-stim']}

setup_kwargs = {
    'name': 'quri-parts',
    'version': '0.4.1',
    'description': 'Platform-independent quantum computing library',
    'long_description': '# QURI Parts\n\n\nQURI Parts is an open source library suite for creating and executing quantum algorithms on various quantum computers and simulators. QURI Parts focuses on the followings:\n\n- **Modularity and extensibility**: It provides small parts with which you can assemble your own algorithms. You can also use ready-made algorithms, customizing their details by replacing sub components easily.\n- **Platform independence**: Once you assemble an algorithm with QURI Parts, you can execute it on various quantum computers or simulators without modifying the main algorithm code. Typically you only need to replace a few lines to switch to a different device or simulator.\n- **Performance**: When dealing with a simulator, it is often the case that classical computation before and after quantum circuit simulation (such as data preparation and post processing) takes considerable time, spoiling performance of the simulator. We put an emphasis on computational performance and try to get the most out of simulators.\n\n\n## Covered areas and components\n\nCurrent QURI Parts covers the following areas, provided as individual components.\nPlease note that more components will be added in future.\nYou are also encouraged to propose or author new components as necessary.\n\n- Core components\n  - `quri-parts-circuit`: Quantum circuit\n      - Gate, circuit, noise etc.\n  - `quri-parts-core`: General components\n      - Operator, state, estimator, sampler etc.\n- Platform (device/simulator) support\n  - Quantum circuit simulators\n      - `quri-parts-qulacs`: [Qulacs](https://github.com/qulacs/qulacs)\n      - `quri-parts-stim`: [Stim](https://github.com/quantumlib/Stim)\n  - Quantum platforms/SDKs\n      - `quri-parts-braket`: [Amazon Braket SDK](https://github.com/aws/amazon-braket-sdk-python)\n      - `quri-parts-cirq`: [Cirq](https://quantumai.google/cirq) (Only circuit conversion is supported yet)\n      - `quri-parts-qiskit`: [Qiskit](https://qiskit.org/) (Circuit conversion and execution are not supported yet)\n- `quri-parts-algo`: Algorithms\n  - Ansatz, optimizer, error mitigation etc.\n- Chemistry\n  - `quri-parts-chem`: General concepts\n      - Fermion-qubit mapping etc.\n  - Library support\n      - `quri-parts-openfermion`: [OpenFermion](https://quantumai.google/openfermion)\n\n\n## Installation\n\nQURI Parts requires Python 3.9.8 or later.\n\nUse `pip` to install QURI Parts.\nDefault installation only contains components not depending specific platforms (devices/simulators) or external libraries.\nYou need to specify *extras* with square brackets (`[]`) to use those platforms and external libraries with QURI Parts:\n\n```\n# Default installation, no extras\npip install quri-parts\n\n# Use Qulacs, a quantum circuit simulator\npip install "quri-parts[qulacs]"\n\n# Use Amazon Braket SDK\npip install "quri-parts[braket]"\n\n# Use Qulacs and OpenFermion, a quantum chemistry library for quantum computers\npip install "quri-parts[qulacs,openfermion]"\n```\n\nCurrently available extras are as follows:\n\n- `qulacs`\n- `braket`\n- `qiskit`\n- `cirq`\n- `openfermion`\n- `stim`\n\nYou can also install individual components (`quri-parts-*`) directly.\nIn fact, `quri-parts` is a meta package, a convenience method to install those individual components.\n\n### Installation from local source tree\n\nIf you check out the QURI Parts repository and want to install from that local source tree, you can use `requirements-local.txt`.\nIn `requirements-local.txt`, optional components are commented out, so please uncomment them as necessary.\n\n```\npip install -r requirements-local.txt\n```\n\n\n## Documentation and tutorials\n\nDocumentation of QURI Parts is available at <https://quri-parts.qunasys.com>.\n[Tutorials](https://quri-parts.qunasys.com/tutorials.html) would be a good starting point.\n\n## Release notes\n\nSee [Releases page](https://github.com/QunaSys/quri-parts/releases) on GitHub.\n\n\n## Contribution guidelines\n\nIf you are interested in contributing to QURI Parts, please take a look at our [contribution guidelines](CONTRIBUTING.md).\n\n\n## Authors\n\nQURI Parts developed and maintained by [QunaSys Inc.](https://qunasys.com/en). All contributors can be viewed on [GitHub](https://github.com/QunaSys/quri-parts/graphs/contributors).\n\n\n## License\n\nQURI Parts is licensed under [Apache License 2.0](https://github.com/QunaSys/quri-parts/blob/main/LICENSE).\n',
    'author': 'QURI Parts Authors',
    'author_email': 'opensource@qunasys.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/QunaSys/quri-parts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9.8,<3.12',
}


setup(**setup_kwargs)
