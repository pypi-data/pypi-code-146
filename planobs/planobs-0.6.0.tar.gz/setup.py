# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['planobs']

package_data = \
{'': ['*'], 'planobs': ['data/*', 'data/references/*']}

install_requires = \
['Shapely>=1.8.2,<2.0.0',
 'astroplan>=0.7',
 'astropy>=5.0,<6.0',
 'bs4>=0.0.1,<0.0.2',
 'cligj>=0.7.2,<0.8.0',
 'geopandas>=0.11,<0.13',
 'gunicorn>=20.1.0,<21.0.0',
 'lxml>=4.9.1,<5.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'mypy>=0.991,<0.992',
 'pandas>=1.4.3,<2.0.0',
 'penquins>=2.1.0,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'slackclient>=2.9.4,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'types-requests>=2.28.11.5,<3.0.0.0',
 'ztfquery>=1.18.4,<2.0.0']

extras_require = \
{':extra == "slack"': ['Flask>=2.1.3,<3.0.0',
                       'slack>=0.0.2,<0.0.3',
                       'slackeventsapi>=3.0.1,<4.0.0']}

setup_kwargs = {
    'name': 'planobs',
    'version': '0.6.0',
    'description': 'Plan observations with the Zwicky Transient Facility',
    'long_description': '# planobs\nToolset for planning and triggering observations with ZTF. GCN parsing is currently only implemented for IceCube alerts.\n\nIt checks if the object is observable with a maximum airmass on a given date, plots the airmass vs. time, computes two optimal (minimal airmass at night) observations of 300s in g- and r and generate the ZTF field plots for all fields having a reference. There is also the option to create a longer (multiday) observation plan.\n\n[![CI](https://github.com/simeonreusch/planobs/actions/workflows/continous_integration.yml/badge.svg)](https://github.com/simeonreusch/planobs/actions/workflows/continous_integration.yml)\n[![Coverage Status](https://coveralls.io/repos/github/simeonreusch/planobs/badge.svg?branch=main)](https://coveralls.io/github/simeonreusch/planobs?branch=main)\n[![PyPI version](https://badge.fury.io/py/planobs.svg)](https://badge.fury.io/py/planobs)\n[![DOI](https://zenodo.org/badge/512753573.svg)](https://zenodo.org/badge/latestdoi/512753573)\n\n# Requirements\n[ztfquery](https://github.com/mickaelrigault/ztfquery) for checking if fields have a reference.\n\nplanobs requires Python 3.10.\n\n# Installation\nUsing Pip: ```pip install planobs```.\n\nOtherwise, you can clone the repository: ```git clone https://github.com/simeonreusch/planobs```, followed by ```poetry install``` This also gives you access to the Slackbot. Note for ARM-based macs: The install of `fiona` might fail. In that case, consider using a `conda` and issuing `conda install -c conda-forge fiona` before running `poetry`.\n\n# General usage\n```python\nfrom planobs.plan import PlanObservation\n\nname = "testalert" # Name of the alert object\ndate = "2020-05-05" #This is optional, defaults to today\nra = 133.7\ndec = 13.37\n\nplan = PlanObservation(name=name, date=date, ra=ra, dec=dec)\nplan.plot_target() # Plots the observing conditions\nplan.request_ztf_fields() # Checks in which ZTF fields this \n# object is observable and generates plots for them.\n```\nThe observation plot and the ZTF field plots will be located in the current directory/[name]\n![](examples/figures/observation_plot_generic.png)\n\nNote: Checking if fields have references requires ztfquery, which needs IPAC credentials.\n\n# Usage for IceCube alerts\n```python\nfrom planobs.plan import PlanObservation\n\nname = "IC201007A" # Name of the alert object\ndate = "2020-10-08" #This is optional, defaults to today\n\n# No RA and Dec values are given, because we set alertsource to icecube, which leads to automatic GCN parsing.\n\nplan = PlanObservation(name=name, date=date, alertsource="icecube")\nplan.plot_target() # Plots the observing conditions.\nplan.request_ztf_fields() # Checks which ZTF fields cover the target (and have references).\nprint(plan.recommended_field) # This give you the field with the most overlap.\n```\n![](examples/figures/observation_plot_icecube.png)\n![](examples/figures/grid_icecube.png)\n\n# Triggering ZTF\n\n`planobs` can be used to schedule ToO observations with ZTF. \nThis is done through API calls to the `Kowalski` system, managed by the Kowalski Python API [penquins](https://github.com/dmitryduev/penquins).\n\nTo use this functionality, you must first configure the connection details. You need both an API token, and to know the address of the Kowalski host address. You can then set these as environment variables:\n\n```bash\nexport KOWALSKI_HOST=something\nexport KOWALSKI_API_TOKEN=somethingelse\n```\n\nYou can then import the Queue class for querying, submitting and deleting ToO triggers:\n\n## Querying\n\n```python\nfrom planobs.api import Queue\n\nq = Queue(user="yourname")\n\nexisting_too_requests = get_too_queues(names_only=True)\nprint(existing_too_requests)\n```\n\n## Submitting\n\n```python\nfrom planobs.api import Queue\n\ntrigger_name = "ToO_IC220513A_test"\n\n# Instantiate the API connection\nq = Queue(user="yourname")\n\n# Add a trigger to the internal submission queue. Filter ID is 1 for r-, 2 for g- and 3 for i-band. Exposure time is given in seconds.\nq.add_trigger_to_queue(\n    trigger_name=trigger_name,\n    validity_window_start_mjd=59719.309333333334,\n    field_id=427,\n    filter_id=1,\n    exposure_time=300,\n)\n\nq.submit_queue()\n\n# Now we verify that our trigger has been successfully submitted\nexisting_too_requests = get_too_queues(names_only=True)\nprint(existing_too_requests)\nassert trigger_name in existing_too_requests\n```\n\n## Deleting\n```python\nfrom planobs.api import Queue\n\nq = Queue(user="yourname")\n\ntrigger_name = "ToO_IC220513A_test"\n\nres = q.delete_trigger(trigger_name=trigger_name)\n```\n\n# Citing the code\n\nIf you use this code, please cite it! A DOI is provided by Zenodo, which can reference both the code repository and specific releases:\n\n[![DOI](https://zenodo.org/badge/512753573.svg)](https://zenodo.org/badge/latestdoi/512753573)\n\n# Contributors\n\n* Simeon Reusch [@simeonreusch](https://github.com/simeonreusch)\n* Robert Stein [@robertdstein](https://github.com/robertdstein)',
    'author': 'Simeon Reusch',
    'author_email': 'simeon.reusch@desy.de',
    'maintainer': 'Simeon Reusch',
    'maintainer_email': 'simeon.reusch@desy.de',
    'url': 'https://github.com/simeonreusch/planobs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
