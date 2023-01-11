# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skyplane',
 'skyplane.api',
 'skyplane.broadcast.gateway',
 'skyplane.broadcast.gateway.operators',
 'skyplane.cli',
 'skyplane.cli.experiments',
 'skyplane.cli.impl',
 'skyplane.compute',
 'skyplane.compute.aws',
 'skyplane.compute.azure',
 'skyplane.compute.gcp',
 'skyplane.data',
 'skyplane.gateway',
 'skyplane.obj_store',
 'skyplane.planner',
 'skyplane.utils']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.1.0',
 'cryptography>=1.4.0',
 'pandas>=1.0.0',
 'paramiko>=2.7.2',
 'questionary>=1.8.0',
 'requests>=2.23.0',
 'rich>=9.0.0',
 'sshtunnel>=0.3.0',
 'typer>=0.4.0']

extras_require = \
{':extra == "aws" or extra == "all"': ['boto3>=1.16.0'],
 'all': ['azure-identity>=1.0.0',
         'azure-mgmt-authorization>=1.0.0',
         'azure-mgmt-compute>=24.0.0',
         'azure-mgmt-network>=10.0.0',
         'azure-mgmt-resource>=11.0.0',
         'azure-mgmt-storage>=11.0.0',
         'azure-mgmt-subscription>=1.0.0',
         'azure-storage-blob>=12.0.0',
         'google-api-python-client>=2.0.2',
         'google-auth>=2.0.0',
         'google-cloud-compute>=1.0.0',
         'google-cloud-storage>=1.30.0'],
 'azure': ['azure-identity>=1.0.0',
           'azure-mgmt-authorization>=1.0.0',
           'azure-mgmt-compute>=24.0.0',
           'azure-mgmt-network>=10.0.0',
           'azure-mgmt-resource>=11.0.0',
           'azure-mgmt-storage>=11.0.0',
           'azure-mgmt-subscription>=1.0.0',
           'azure-storage-blob>=12.0.0'],
 'gateway': ['flask>=2.1.2,<3.0.0',
             'lz4>=4.0.0,<5.0.0',
             'pynacl>=1.5.0,<2.0.0',
             'pyopenssl>=22.0.0,<23.0.0',
             'werkzeug>=2.1.2,<3.0.0'],
 'gcp': ['google-api-python-client>=2.0.2',
         'google-auth>=2.0.0',
         'google-cloud-compute>=1.0.0',
         'google-cloud-storage>=1.30.0'],
 'solver': ['cvxpy[cvxopt]>=1.1.0',
            'graphviz>=0.15',
            'matplotlib>=3.0.0',
            'numpy>=1.19.0']}

entry_points = \
{'console_scripts': ['skylark = skyplane.cli.cli:app',
                     'skyplane = skyplane.cli.cli:app']}

setup_kwargs = {
    'name': 'skyplane-nightly',
    'version': '0.2.1.dev20230111',
    'description': 'Skyplane efficiently transports data between cloud regions and providers.',
    'long_description': '<picture>\n    <source srcset="docs/_static/logo-dark-mode.png" media="(prefers-color-scheme: dark)">\n    <img src="docs/_static/logo-light-mode.png" width="300" />\n</picture>\n\n[![Join Slack](https://img.shields.io/badge/-Join%20Skyplane%20Slack-blue?logo=slack)](https://join.slack.com/t/skyplaneworkspace/shared_invite/zt-1cxmedcuc-GwIXLGyHTyOYELq7KoOl6Q)\n[![integration-test](https://github.com/skyplane-project/skyplane/actions/workflows/integration-test.yml/badge.svg)](https://github.com/skyplane-project/skyplane/actions/workflows/integration-test.yml)\n[![docker](https://github.com/skyplane-project/skyplane/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/skyplane-project/skyplane/actions/workflows/docker-publish.yml)\n[![docs](https://readthedocs.org/projects/skyplane/badge/?version=latest)](https://skyplane.readthedocs.io/en/latest/?badge=latest)\n\n**🔥 Blazing fast bulk data transfers between any cloud 🔥**\n\nSkyplane is a tool for blazingly fast bulk data transfers between object stores in the cloud. It provisions a fleet of VMs in the cloud to transfer data in parallel while using compression and bandwidth tiering to reduce cost.\n\nSkyplane is:\n1. 🔥 Blazing fast ([110x faster than AWS DataSync](https://skyplane.org/en/latest/benchmark.html))\n2. 🤑 Cheap (4x cheaper than rsync)\n3. 🌐 Universal (AWS, Azure and GCP)\n\nYou can use Skyplane to transfer data: \n* between object stores within a cloud provider (e.g. AWS us-east-1 to AWS us-west-2)\n* between object stores across multiple cloud providers (e.g. AWS us-east-1 to GCP us-central1)\n* between local storage and cloud object stores (experimental)\n\nSkyplane currently supports the following source and destination endpoints (any source and destination can be combined): \n\n| Endpoint           | Source             | Destination        |\n|--------------------|--------------------|--------------------|\n| AWS S3             | :white_check_mark: | :white_check_mark: |\n| Google Storage     | :white_check_mark: | :white_check_mark: |\n| Azure Blob Storage | :white_check_mark: | :white_check_mark: |\n| Local Disk         | :white_check_mark: | (in progress)      |\n\nSkyplane is an actively developed project. It will have 🔪 SHARP EDGES 🔪. Please file an issue or ask the contributors via [the #help channel on our Slack](https://join.slack.com/t/skyplaneworkspace/shared_invite/zt-1cxmedcuc-GwIXLGyHTyOYELq7KoOl6Q) if you encounter bugs.\n\n# Resources \n- [Quickstart](#quickstart)\n- [Contributing](https://skyplane.org/en/latest/contributing.html)\n- [Roadmap](https://skyplane.org/en/latest/roadmap.html)\n- [Slack Community](https://join.slack.com/t/skyplaneworkspace/shared_invite/zt-1cxmedcuc-GwIXLGyHTyOYELq7KoOl6Q)\n\n# Quickstart\n\n## 1. Installation\nWe recommend installation from PyPi:\n```\n$ pip install skyplane[aws]\n\n# install support for other clouds as needed:\n#   $ pip install skyplane[azure]\n#   $ pip install skyplane[gcp]\n#   $ pip install skyplane[all]\n```\n\nSkyplane supports AWS, Azure, and GCP. You can install Skyplane with support for one or more of these clouds by specifying the corresponding extras. To install two out of three clouds, you can run `pip install skyplane[aws,azure]`.\n\n*GCP support on the M1 Mac*: If you are using an M1 Mac with the arm64 architecture and want to install GCP support for Skyplane, you will need to install as follows\n`GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1 GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1 pip install skyplane[aws,gcp]`\n\n## 2. Setup Cloud Credentials \n\nSkyplane needs access to cloud credentials to perform transfers. To get started with setting up credentials, make sure you have cloud provider CLI tools installed:\n\n```\n---> For AWS:\n$ pip install awscli\n\n---> For Google Cloud:\n$ pip install gcloud\n\n---> For Azure:\n$ pip install azure\n```\nOnce you have the CLI tools setup, log into each cloud provider\'s CLI:\n```\n---> For AWS:\n$ aws configure\n\n---> For Google Cloud:\n$ gcloud auth application-default login\n\n---> For Azure:\n$ az login\n```\nAfter authenticating with each cloud provider, you can run `skyplane init` to create a configuration file for Skyplane.\n\n```bash\n$ skyplane init\n```\n<details>\n<summary>skyplane init output</summary>\n<br>\n\n```\n$ skyplane init\n\n====================================================\n _____ _   ____   _______ _       ___   _   _  _____\n/  ___| | / /\\ \\ / / ___ \\ |     / _ \\ | \\ | ||  ___|\n\\ `--.| |/ /  \\ V /| |_/ / |    / /_\\ \\|  \\| || |__\n `--. \\    \\   \\ / |  __/| |    |  _  || . ` ||  __|\n/\\__/ / |\\  \\  | | | |   | |____| | | || |\\  || |___\n\\____/\\_| \\_/  \\_/ \\_|   \\_____/\\_| |_/\\_| \\_/\\____/\n====================================================\n\n\n(1) Configuring AWS:\n    Loaded AWS credentials from the AWS CLI [IAM access key ID: ...XXXXXX]\n    AWS region config file saved to /home/ubuntu/.skyplane/aws_config\n\n(2) Configuring Azure:\n    Azure credentials found in Azure CLI\n    Azure credentials found, do you want to enable Azure support in Skyplane? [Y/n]: Y\n    Enter the Azure subscription ID: [XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX]:\n    Azure region config file saved to /home/ubuntu/.skyplane/azure_config\n    Querying for SKU availbility in regions\n    Azure SKU availability cached in /home/ubuntu/.skyplane/azure_sku_mapping\n\n(3) Configuring GCP:\n    GCP credentials found in GCP CLI\n    GCP credentials found, do you want to enable GCP support in Skyplane? [Y/n]: Y\n    Enter the GCP project ID [XXXXXXX]:\n    GCP region config file saved to /home/ubuntu/.skyplane/gcp_config\n\nConfig file saved to /home/ubuntu/.skyplane/config\n```\n\n</details>\n\n## 3. Run Transfers \n\nWe’re ready to use Skyplane! Let’s use `skyplane cp` to copy files from AWS to GCP:\n```\nskyplane cp s3://... gs://...\n```\nTo transfer only new objects, you can instead use `skyplane sync`:\n```\n$ skyplane sync s3://... gs://...\n```\n\nYou can configure Skyplane to use more VMs per region with the `-n` flag. For example, to double the transfer speed with two VMs, run: \n```\n$ skyplane cp -r s3://... s3://... -n 2\n```\n\n## 4. Clean Up \nSkyplane will automatically attempt to terminate VMs that it starts, but to double check and forcefuly terminate all VMs, run `skyplane deprovision`.\n\n# Technical Details\nSkyplane is based on research at UC Berkeley into accelerated networks between cloud providers. Under the hood, Skyplane starts a fleet of VMs in the source and destination regions. It then uses a custom TCP protocol to accelerate the transfer between the VMs. Skyplane may use a L7 overlay network to route traffic around congested network hot spots. \n\n<img src="docs/_static/skyplane-data-plane.png" width="384" />\n\nFor more details on Skyplane, see: \n- [Technical Talk](https://skyplane.org/en/latest/architecture.html)\n- [NSDI \'23 Paper](https://arxiv.org/abs/2210.07259)\n\n\n',
    'author': 'Skyplane authors',
    'author_email': 'skyplaneproject@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://skyplane.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
