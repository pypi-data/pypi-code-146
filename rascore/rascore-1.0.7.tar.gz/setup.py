# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rascore',
 'rascore.util.PDBrenum',
 'rascore.util.PDBrenum.src.download',
 'rascore.util.PDBrenum.src.renum.PDB',
 'rascore.util.PDBrenum.src.renum.mmCIF',
 'rascore.util.PDBrenum.src.renum.shared',
 'rascore.util.constants',
 'rascore.util.functions',
 'rascore.util.pages',
 'rascore.util.pipelines',
 'rascore.util.scripts']

package_data = \
{'': ['*'],
 'rascore': ['.streamlit/*',
             'util/*',
             'util/data/*',
             'util/data/rascore_cluster/*',
             'util/data/rascore_cluster/SW1/*',
             'util/data/rascore_cluster/SW1/Disordered.0P/*',
             'util/data/rascore_cluster/SW1/Disordered.2P/*',
             'util/data/rascore_cluster/SW1/Disordered.3P/*',
             'util/data/rascore_cluster/SW1/Y32in.0P/*',
             'util/data/rascore_cluster/SW1/Y32in.2P/*',
             'util/data/rascore_cluster/SW1/Y32in.3P/*',
             'util/data/rascore_cluster/SW1/Y32out.0P/*',
             'util/data/rascore_cluster/SW1/Y32out.2P/*',
             'util/data/rascore_cluster/SW1/Y32out.3P/*',
             'util/data/rascore_cluster/SW2/*',
             'util/data/rascore_cluster/SW2/Disordered.0P/*',
             'util/data/rascore_cluster/SW2/Disordered.2P/*',
             'util/data/rascore_cluster/SW2/Disordered.3P/*',
             'util/data/rascore_cluster/SW2/Y71in.0P/*',
             'util/data/rascore_cluster/SW2/Y71in.2P/*',
             'util/data/rascore_cluster/SW2/Y71in.3P/*',
             'util/data/rascore_cluster/SW2/Y71out.0P/*',
             'util/data/rascore_cluster/SW2/Y71out.2P/*',
             'util/data/rascore_cluster/SW2/Y71out.3P/*'],
 'rascore.util.PDBrenum': ['src/*', 'src/renum/*']}

install_requires = \
['Bio==1.3.3',
 'Pillow==9.0.1',
 'lxml==4.6.5',
 'matplotlib==3.3.4',
 'matplotlib_venn==0.11.6',
 'numpy==1.21',
 'pandas==1.3.5',
 'pendulum==2.1.2',
 'py3Dmol==2.0.0.post2',
 'pyfiglet==0.8.post1',
 'rdkit_pypi==2021.9.5.1',
 'requests==2.25.1',
 'scipy==1.6.2',
 'seaborn==0.11.1',
 'statannot==0.2.3',
 'statsmodels==0.13.1',
 'stmol==0.0.7',
 'streamlit==1.8.1',
 'tqdm==4.59.0']

entry_points = \
{'console_scripts': ['rascore = rascore.rascore_cli:cli']}

setup_kwargs = {
    'name': 'rascore',
    'version': '1.0.7',
    'description': 'A tool for analyzing RAS protein structures',
    'long_description': None,
    'author': 'mitch-parker',
    'author_email': 'mip34@drexel.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
