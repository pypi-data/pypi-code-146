# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dace_query',
 'dace_query.astrometry',
 'dace_query.atmosphericSpectroscopy',
 'dace_query.catalog',
 'dace_query.cheops',
 'dace_query.exoplanet',
 'dace_query.imaging',
 'dace_query.lossy',
 'dace_query.monitoring',
 'dace_query.opacity',
 'dace_query.opendata',
 'dace_query.photometry',
 'dace_query.population',
 'dace_query.spectroscopy',
 'dace_query.sun',
 'dace_query.target',
 'dace_query.tess']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.1.1,<6.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'dace-query',
    'version': '1.0.1',
    'description': 'The dace-query lets easily query DACE and access public and private data using a simple utility tool.',
    'long_description': 'dace-query\n##########\n\nDescription\n***********\nThe dace-query lets easily query DACE and access public and private data using a simple utility tool.\n\nInstallation\n************\n\nThe dace-query is available on PyPi and can be installed using `pip <https://pypi.org/project/pip/>`_ or `conda <https://www.anaconda.com>`_:\n\n\n.. code-block:: bash\n\n    # Install using pip\n    pip install dace-query\n\n    # Update using pip\n    pip install dace-query --upgrade\n\n.. code-block:: bash\n\n    # Install using conda\n    # First, create a conda environment\n    conda create -n <env_name> python=3.9 # python version equal or upper than 3.9\n    # Second, activate the environment\n    conda activate <env_name>\n    # Finally, install using anaconda pip\n    pip install dace-query\n\nMake sure the API is installed correctly :\n\n.. code-block:: python\n\n    # Import dace\n    import dace_query\n\n    # List content of the dace package\n    help(dace)\n\nAuthentication\n**************\n\nIn order to access the private data of DACE, an authentication system has been implemented.\nThis one works very simply, it just requires three things detailed in the following subsections:\n\n\n- A DACE account\n- An API key\n- A local .dacerc file\n\n\n.. _create-account:\n\n1. Create an account\n====================\nRegister on the `DACE web portal <https://dace.unige.ch/createAccount/>`_ with a university email address.\n\n.. _api-key:\n\n2. Generate the DACE API key\n============================\nTo obtain an API key:\n\n    1.  Login on DACE (https://dace.unige.ch)\n    2.  Go to the user profile\n    3.  Click on [Generate a new API key]\n    4.  Copy this new API key into the .dacerc file\n\n\n.. _dacerc:\n\n3. The .dacerc file\n===================\nThe **.dacerc** file, (**you have to create it**), located by default in the home directory (~/.dacerc) and in TOML\nformat, defines a user section with a key-value pair specifying the user\'s API key (see below).\n\n.. code-block:: cfg\n\n    [user]\n    key = apiKey:<xxx-xxx-xxx>\n\nFor example, if your API key is 12345678-1234-5678-1234-567812345678, then the .dacerc file will be :\n\n.. code-block:: cfg\n\n    [user]\n    key = apiKey:12345678-1234-5678-1234-567812345678\n\nTo create the .dacerc file on Linux or macOs, open a terminal window and type :\n\n.. code-block:: bash\n\n    printf \'[user]\\nkey = apiKey:%s\\n\' "your-api-key-here" > ~/.dacerc\n\nQuickstart\n**********\n\n.. code-block:: python\n\n    # Import the ready-to-use exoplanet instance\n    from dace_query.exoplanet import Exoplanet\n\n    # Retrieve data from the exoplanet database\n    result: dict = Exoplanet.query_database(limit=10, output_format=\'dict\')\n\n    # Get the planet names\n    planet_names: list = result.get(\'obj_id_catname\')\n\n    # Print the planet names\n    print(planet_names)\n\n\nFor more examples of uses, such as **filtering bad quality data** (see Usage examples)\n\nContact\n*******\n\nIn case of questions, proposals or problems, feel free to contact the `DACE support <mailto:dace-support@unige.ch>`_ .\n\nLinks\n*****\n* `DACE website <https://dace.unige.ch>`_\n',
    'author': 'dace-team',
    'author_email': 'dace-support@unige.ch',
    'maintainer': 'dace-team',
    'maintainer_email': 'dace-support@unige.ch',
    'url': 'https://dace.unige.ch/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
