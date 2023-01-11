# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recomb_to_s3', 'recomb_to_s3.migrations']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.47,<2.0.0',
 'django-storages>=1.13.2,<2.0.0',
 'django>=4.1.5,<5.0.0']

setup_kwargs = {
    'name': 'recomb-to-s3',
    'version': '0.1.3',
    'description': 'package to save files in s3 in a simple way.',
    'long_description': '# Recomb to S3\n\n\nInstallation\n============\nInstalling from PyPI is as easy as doing:\n\n```bash\n\n  pip install recomb-to-s3\n\n```\n\ncreate the following environment variables in your settings:\n\n```python\n\n    AWS_ACCESS_KEY_ID="__your_secret_id__"\n    AWS_SECRET_ACCESS_KEY="__your_secret_key__"\n    AWS_STORAGE_BUCKET_NAME="__your_bucket_name__"\n    AWS_S3_SIGNATURE_VERSION="s3v4"\n    AWS_S3_REGION_NAME="__your_region_name__"\n    AWS_S3_FILE_OVERWRITE=False # true if you want to write over the file in s3\n    AWS_DEFAULT_ACL = "public-read" # to have access by the django admin\n    DEFAULT_FILE_STORAGE="storages.backends.s3boto3.S3Boto3Storage"\n\n```\n\nadd recomb_to_s3 and storages in your installed apps\n\n```python\n\nINSTALLED_APPS = [\n    "storages",\n    "recomb_to_s3",\n]\n\n```\nrun the migration\n\n```python\n\npython manage.py migrate\n\n```\nAbout\n=====\n\nThe library aims to facilitate the sending of python dictionaries to an amazon s3 backet, however it is possible to send any type of file, or you can import the AbstractRecombToS3 class and add or remove fields according to your needs.\n\n\nHow To Use\n=====\n\nthe most basic way to use this package is very simple, just import the "send_dict_to_s3" function and use it as in the example below.\n\n```Python\nfrom recomb_to_s3.contrib import send_dict_to_s3\n\ndata = {"test": "test"}\n\nmy_model = send_dict_to_s3(data=data, file_name="my_file.json", author=None)\n\n```\n\nDependencies\n=====\n\n```toml\n[tool.dependencies]\npython = "^3.10"\nboto3 = "^1.26.47"\ndjango-storages = "^1.13.2"\ndjango = "^4.1"\n```\n\n\nContributing\n=====\n\n\n[<img src="https://avatars.githubusercontent.com/u/52933958?v=4" width=40><br><sub>Alexandre Jastrow da Cruz</sub>](https://github.com/alexandrejastrow)\n',
    'author': 'alexandrejastrow',
    'author_email': 'alexandre.jastrow@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
