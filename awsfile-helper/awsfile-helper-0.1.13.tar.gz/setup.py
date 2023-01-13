# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsfile_helper',
 'awsfile_helper.bp',
 'awsfile_helper.dmo',
 'awsfile_helper.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'boto3']

setup_kwargs = {
    'name': 'awsfile-helper',
    'version': '0.1.13',
    'description': 'AWS File Helper for Easier I/O',
    'long_description': '# AWS File Helper (awsfile-helper)\nContent Management and Retrieval for Cloud and Local Storage\n\n## Code Usage (Authorization)\nYou must have an AWS Access Key and Secret Access key to connect to AWS.\n\nUpon obtaining these keys, use\n```python\nfrom baseblock import CryptoBase\n\nos.environ[\'AWS_ACCESS_KEY\'] = CryptoBase().encrypt_str(\'<my-access-key>\')\nos.environ[\'AWS_SECRET_KEY\'] = CryptoBase().encrypt_str(\'<my-secret-key>\')\n```\n\nThis will place your encrypted credentials into the environment.\n\nThe `AwsAPI` class will retrieve and decrypt these credentials to login.\n\n## Code Usage (General)\nThe following code will retrieve any file:\n```python\nfrom awsfile_helper import FindOwlFile\n\nd_cloud_file = FindS3File(\n    file_name=\'config/graphviz/stylesheets/nlu\',\n    file_ext=\'yaml\', file_version=\'0.1.0\').process()\n```\nThe bucket is assumed to be `data-core-bast`.\n\nWe can modify this assumption down the road if we create new buckets for different clients, etc.\n\nA file may also be retrieved without a version, like this:\n```python\nd_cloud_file = FindS3File(\n    file_name=\'config/graphviz/stylesheets/nlu\',\n    file_ext=\'yaml\').process()\n```\n\nIn that case, the system will first look in the environment, using a key configuration that relies on the `file_name` like this: `CONFIG_GRAPHVIZ_STYLESHEETS_NLU_VERSION`.  If no value is found in the environment, the system will consider this a _wildcard_ match and set the version to `*`.  This forces the system to list the contents of the qualified path and choose the latest version.  This operation takes an additional 2-3 milliseconds, assuming the network is running smoothly.\n\n\n## Code Usage (Ontologies)\nOntologies require a special finder class, because we typically have two files we want to retrieve - an OWL model and a TXT file with synonyms.\n\nTherefore, assume that an S3 bucket exists with two files we want to retrieve: `syllabus.owl` and `syllabus.txt`.\n\nThe following code will retrieve these files:\n```python\nfrom awsfile_helper import FindOwlFile\n\nd_cloud_file = FindOwlFile(file_name=\'syllabus\', version=\'0.1.0\').process()\n```\n\nNote that we did not specify the file extension within the `file_name` variable.\n\nIt is permissible to specify explicit file names such as `syllabus.txt` or partial file names such.\n\nThe result dictionary is keyed by file name and (with redacted contents) looks like this:\n```json\n{\n    "owl": {\n        "path": "<local path to OWL file">,\n        "version": "<version of OWL file>",\n        "contents": "<contents of OWL file>"\n    },\n    "txt": {\n        "path": "<local path to txt file">,\n        "version": "<version of txt file>",\n        "contents": "<contents of txt file>"\n    }\n}\n```\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/awsfile-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
