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
    'version': '1.0.1.dev1',
    'description': '`opensearch-reindex` is a Python library that serves to help streamline reindexing data from one OpenSearch index to another.',
    'long_description': '# opensearch-reindexer\n\n`opensearch-reindexer` is a Python library that serves to help streamline reindexing data from one OpenSearch \nindex to another using either the native OpenSearch Reindex API or Python, the OpenSearch Scroll API and Bulk inserts.\n\n## Features\n* Native OpenSearch Reindex API and Python based reindexing using OpenSearch Scroll API\n* Migrate data from one index to another in the same cluster\n* Migrate data from one index to another in a different cluster\n* Revision history\n* Run multiple migrations one after another\n* Transform documents using native OpenSearch Reindex API or Python using Scoll API and Bulk inserts\n* Source indices/data is never modified or removed\n\n## Getting started\n\n### 1. Install opensearch-reindexer\n\n`pip install opensearch-reindexer`\n\nor\n\n`poetry add opensearch-reindexer`\n\n### 2. Initialize project\n\n`reindexer init`\n\n### 3. Configure your source_client in `./migrations/env.py`\nYou only need to configure `destination_client` if you are migrating data from one cluster to another.\n\n### 4. Create `reindexer_version` index\n\n`reindexer init-index`\n\nThis will use your `source_client` to create a new index named \'reindexer_version\' and insert a new document specifying the revision version.\n`{"versionNum": 0}`. `reindexer_version` is used to keep track of which revisions have been run.\n\nWhen reindexing from one cluster to another, migrations should be run first (step 8) before initializing the destination cluster with:\n`reindexer init-index`\n\n### 5. Create revision\nTwo revision types are supported, `painless` which uses the native OpenSearch Reindex API, and `python` which using\nthe OpenSearch Scroll API and Bulk inserts. `painless` revisions are recommended as they are more performant than \n`python` revisions. You don\'t have to use one or the other; `./migrations/versions/` can contain a combination of \nboth `painless` and `python` revisions.\n\n#### To create a `painless` revision run:\n\n`reindexer revision \'my revision name\'`\n\n#### To create a `python` revision run:\n\n`reindexer revision \'my revision name\' --language python`\n\nThis will create a new revision file in `./migrations/versions`.\n\nNote: \n1. revision files should not be removed and their names should not be changed once created.\n2. `./migration/migration_template_painless.py` and `./migration/migration_template_python.py` are referenced for each revision.\nYou can modify them if you find yourself making the same changes to revision files.\n\n### 6. Modify your revision file \nNavigate to your revision file `./migrations/versions/1_my_revision_name.py`\n\n#### Painless\nModify `source` and `destination` in `REINDEX_BODY`, you can optionally set `DESTINATION_MAPPINGS`.\n\nTo transform data as data is reindexed, you can use \npainless scripts. For example, the following will convert data in field "c" from an object to a JSON string \nbefore inserting it into index `destination`.\n\n```python\nREINDEX_BODY = {\n    "source": {"index": "reindexer_revision_1"},\n    "dest": {"index": "reindexer_revision_2"},\n    "script": {\n        "lang": "painless",\n        "source": """\n        def jsonString = \'{\';\n        int counter = 1;\n        int size = ctx._source.c.size();\n        for (def entry : ctx._source.c.entrySet()) {\n          jsonString += \'"\'+entry.getKey()+\'":\'+\'"\'+entry.getValue()+\'"\';\n          if (counter != size) {\n            jsonString += \',\';\n          }\n          counter++;\n        }\n        jsonString += \'}\';\n        ctx._source.c = jsonString;\n        """\n    }\n}\n```\nFor more information on `REINDEX_BODY` see https://opensearch.org/docs/latest/opensearch/reindex-data/\n\n#### Python\nModify `SOURCE_INDEX` and `DESTINATION_INDEX`, you can optionally set `DESTINATION_MAPPINGS`.\n\nTo modify documents as they are being re-indexed to the destination index, update `def transform_document`. For example:\n```python\nclass Migration(BaseMigration):\n    def transform_document(self, doc: dict) -> dict:\n        # Modify this method to transform each document before being inserted into destination index.\n        import json\n        doc[\'c\'] = json.dumps(doc[\'c\'])\n        return doc\n```\n### 7. See an ordered list of revisions that have not be executed\n`reindexer list`\n\n#### 8. Run your migrations\n`reindexer run`\n\nNote: When `reindexer run` is executed, it will compare revision versions in `./migrations/versions/...` to the version number in `reindexer_version` index of the source cluster.\nAll revisions that have not been run will be run one after another. \n',
    'author': 'Kenton Parton',
    'author_email': 'kparton@swiple.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Swiple/opensearch-reindexer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
