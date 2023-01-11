# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_walk_controversy']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'random-walk-controversy',
    'version': '0.1.4',
    'description': "Parallel implementation of Garimella's algorithm to get the RWC score of a network",
    'long_description': '# Random Walk Controversy\n\n[![Tests](https://github.com/bendico765/random_walk_controversy/actions/workflows/github-actions-demo.yml/badge.svg?branch=master)](https://github.com/bendico765/random_walk_controversy/actions/workflows/github-actions-demo.yml)\n\nThis repo contains a parallel implementation of Kiran Garimella\'s algorithm to compute the random walk controversy \nscore of a graph.  \n\nLet _G(V,E)_ be a graph with two partitions _X_ and _Y_; in the paper\n["Quantifying Controversy on Social Media"](https://dl.acm.org/doi/abs/10.1145/3140565) Garimella et al. define the \nRandom Walk Controversy (RWC) measure as follows: _"Consider two random walks, one ending in partition X and one ending \nin partition Y , RWC is the difference of the probabilities of two events: (i) both random walks started from the \npartition they ended in and (ii) both random walks started in a partition other than the one they ended in.”._  \nThe measure is quantified as $RWC = P_{XX}P_{YY} - P_{YX}P_{XY}$ where $P_{AB}$ is the conditional \nprobability $P_{AB} = Pr[\\mbox{start in partition }A \\mid \\mbox{end in partition }B]$.  \n\nSince the probabilities are computed by making simulations consisting in random walks and the simulations are independent\nof each other, they can easily be done in parallel.  \nThe following table shows the performance and results comparison made between the (sequential) \n[implementation](https://github.com/gvrkiran/controversy-detection) provided by one of the original authors and this \nimplementation. The datasets can be found in the same repo as the original authors\' implementation.\n\n| **Dataset**    | **Seq. time (s)** | **Seq. RWC score** | **Par. time (s)** | **Par. RWC score** | **Speedup** |\n|----------------|-------------------|--------------------|-------------------|--------------------|-------------|\n| baltimore      | 618               | 0.869              | 71                | 0.872              | 8.70        |\n| beefban        | 128               | 0.873              | 19                | 0.882              | 6.73        |\n| gunsense       | 2232              | 0.851              | 221               | 0.853              | 10.10       |\n| indiana        | 229               | 0.720              | 37                | 0.727              | 6.19        |\n| indiasdaughter | 490               | 0.825              | 62                | 0.832              | 7.90        |\n\nBeside the evident speedup obtained by exploiting a multicore architecture, we can see that the sequential and parallel\nversions almost converge to the same results.\n\n## Installation\nTo install the latest version of the library just download (or clone) the current project, open a terminal and run the \nfollowing commands:\n```\npip install -r requirements.txt\npip install .\n```\nAlternatively use pip\n```\npip install random-walk-controversy\n```\n\n## Usage\n### Command line interface\n```\npython3 -m random_walk_controversy [-h] [-v] [-l] edgelist community1_nodelist community2_nodelist percent n\n```\nMore info about the parameters can be fetched by using the ```-h``` option.  \nThe option  ```-v``` can be used to increase output verbosity and print, alongside the rwc score, the statistics about\nrandom walks. If not specified, only the RWC score is printed out.  \nFinally, the ```-l``` option displays a log on the terminal everytime a simulation is completed; I have found this option \npretty usefully since it allows to estimate the time for the algorithm to complete and understand if the algorithm got \nstuck.\n\n\n### Python library\nAfter the installation, it is possible to compute the rwc score directly in the python interpreter by using the function\n```get_rwc``` inside the ```random_walk_controversy``` package.\n\n#### Example\n```python\n>>> from random_walk_controversy import get_rwc\n>>> graph = read_edgelist()\n>>> side1_nodes = read_nodelist()  # list of nodes belonging to partition 1\n>>> side2_nodes = read_nodelist()  # list of nodes belonging to partition 2\n>>> node_percentage = 0.3\n>>> number_simulations = 1000\n>>> get_rwc(graph, side1_nodes, side2_nodes, node_percentage, number_simulations)\n76.233\n```\n',
    'author': 'Gianluca Morcaldi',
    'author_email': 'bendico765@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bendico765/random_walk_controversy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
