# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cobra_db', 'cobra_db.scripts']

package_data = \
{'': ['*']}

install_requires = \
['deid>=0.2.36,<0.3.0',
 'dnspython>=2.2.1,<3.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pyaml-env>=1.1.5,<2.0.0',
 'pycryptodome>=3.15.0,<4.0.0',
 'pydicom>=2.3.0,<3.0.0',
 'pymongo[srv]>=4.2.0,<5.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['cobra_group = cobra_db.scripts.stage_2:cli',
                     'cobra_ingest = '
                     'cobra_db.scripts.stage_1_ingest_images:cli',
                     'cobra_pseudonymize = '
                     'cobra_db.scripts.pseudonymize_image_metadata:main']}

setup_kwargs = {
    'name': 'cobra-db',
    'version': '0.0.2',
    'description': 'COnsolidated BReast cancer Analysis DataBase',
    'long_description': '# <img src="static/img/cobra_db.png" alt="" height="30"/> cobra_db\n\n\n\n<center>\n\n[![PyPI version](https://badge.fury.io/py/cobra_db.svg)](https://badge.fury.io/py/cobra_db)\n[![Documentation Status](https://readthedocs.org/projects/cobra-db/badge/?version=latest)](https://cobra-db.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/mammoai/cobra-db/branch/main/graph/badge.svg?token=ASQPS89408)](https://codecov.io/gh/mammoai/cobra-db)\n\n<img src="static/img/cobra_db.png" alt="" height="200"/>\n\n**Co**nsolidated **Br**east Cancer **A**nalysis **D**ata**B**ase\n</center>\n\n\n\n\n## What is ```cobra_db```?\n_cobra_db_ is a python package that allows you to extract DICOM metadata and store it in a MongoDB database. Allowing you to index, transform, and export your medical imaging metadata.\n\nWith cobra_db, you will have more visibility of your data enabling you to get more value from your medical imaging studies.\n\nOnce the metadata is in the database, you can import other text-based information (csv or json) into a custom collection and then run queries. This allows you to mix and match data extracted from different sources in different formats.\n\nFor example, let\'s say you have 1 million mammography DICOM files and you would like to obtain the path of the files that belong to women scanned at an age of between 40 and 50 years old.\n\nIf you had cobra_db, you could run the following query in just a few seconds directly in the mongo shell.\n\n```javascript\ndb.ImageMetadata.find(\n  // filter the data\n  {patient_age:{$gt:40, $lte:50}},\n  // project it into a flat structure\n  {\n    patient_id: "$dicom_tags.PatientID.Value"\n    drive_name: "$file_source.drive_name",\n    rel_path:"$file_source.rel_path",\n  })\n```\nThis would return the patient id, the drive name and the relative path (to the drive) for all the files that match the selection criteria.\n\n## Installation\nIf you already have a working instance of the database, you only need to install the python package.\n\n```bash\n$ pip install cobra_db\n```\n\nIf you would like to create a database from scratch, go ahead and follow the [tutorial](https://cobra-db.readthedocs.io/en/latest/tutorial.html).\n\n## Usage\n\nIf you have an `ImageMetadata` instance id that you would like to access from python.\n\n```python\nfrom cobra_db import Connector, ImageMetadataDao\n\n# the _id of the ImageMetadata instance that you want to access\nim_id = \'62de8e38dc2414586e4ddb25\'\n\n# prompt user for password\nconnector = Connector.get_pass(\n  host=\'my_host.server.com\',\n  port=27017,\n  db_name=\'cobra_db\',\n  username=\'my_user\'\n)\n# connect to the ImageMetadata collection\nim_dao = ImageMetadataDao(connector)\nim = im_dao.get_by_id(im_id)\nprint(im.date.file_source.rel_path)\n\n# this will return\n... rel/path/to/my_file.dcm\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a [Code of Conduct](https://cobra-db.readthedocs.io/en/latest/conduct.html). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cobra_db` was created by Fernando Cossio, Apostolia Tsirikoglou, Annika Gregoorian, Haiko Schurz, and Fredrik Strand. It is licensed under the terms of the Apache License 2.0 license.\n\n## Aknowledgements\n\nThis project has been funded by research grants Regional Cancer Centers in Collaboration 21/00060, and Vinnova 2021-0261.\n',
    'author': 'Fernando Cossio',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
