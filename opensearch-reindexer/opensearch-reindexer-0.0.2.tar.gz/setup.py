# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensearch_reindexer']

package_data = \
{'': ['*']}

install_requires = \
['opensearch-py>=2.0.0,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['reindexer = opensearch_reindexer:app']}

setup_kwargs = {
    'name': 'opensearch-reindexer',
    'version': '0.0.2',
    'description': '`opensearch-reindex` is a Python library that serves to help streamline reindexing data from one OpenSearch index to another.',
    'long_description': '# opensearch-reindex\n\n`opensearch-reindex` is a Python library that serves to help streamline reindexing data from one OpenSearch index to another.\n\n## Features\n* Migrate data from one index to another in the same cluster\n* Migrate data from one index to another in different clusters\n* Revision history\n* Run multiple migrations one after another\n* Transform documents using Python before data is inserted into destination index\n* Source data is never modified or removed\n\n## Getting started\n\n#### 1. Install opensearch-reindex\n\n`pip install opensearch-reindex`\n\nor\n\n`poetry add opensearch-reindex`\n\n#### 2. Initialize project\n\n`reindexer init`\n\n#### 3. Configure your source_client and destination_client in `./migrations/env.py`\n\n#### 4. Create `reindexer_version` index\n\n`reindexer init-index`\n\nThis will use your `source_client` to create a new index named \'reindexer_version\' and insert a new document specifying the revision version.\n`{"versionNum": 0}`\n\nWhen reindexing from one cluster to another, migrations should be run first (step 8) before initializing the destination cluster with:\n`reindexer init-index`\n\n#### 5. Create revision\n\n`reindex revision \'my revision name\'`\n\nThis will create a new revision file in `./migrations/versions`.\n\nNote: revisions files should not be removed and their names should not be changed.\n\n#### 6 Navigate to your revision file `./migrations/versions/1_my_revision_name.py` and set\n`SOURCE_INDEX`, `DESTINATION_INDEX`, you can optionally set `DESTINATION_MAPPINGS`.\n\n#### (Optional) 7. To modify documents as they are being reindexed to the destination index, update `def transform_document` accordingly\n\n#### 8. Run your migrations\n`reindexer run`\n\nNote: When `reindexer run` is executed, it will compare revision versions in `./migrations/versions/...` to the version number in `reindexer_version` index.\nAll revisions that have not been run will be run one after another.\n',
    'author': 'Kenton Parton',
    'author_email': 'kparton@swiple.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
