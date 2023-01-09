# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kada_ge_store_plugin']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity==1.12.0', 'azure-storage-blob==12.14.1']

setup_kwargs = {
    'name': 'kada-ge-store-plugin',
    'version': '0.1.7',
    'description': 'Plugin package for great_expectations to store validation results in a different format in Azure storage.',
    'long_description': "# ge-kada-plugin\n\n### Steps to use the KadaStoreValidationResultsAction from the plugin\n\n1. Install the plugin by `pip install kada-ge-store-plugin`. You can put `kada-ge-store-plugin` in the requirements.txt file for CI/CD operations. You'll also need the following two Azure modules:\n\n    * azure.identity\n    * azure.storage.blob\n\nThese will be installed as dependencies so you won't have to install them.\n\n2. In your required `checkpoint`, add the following action to your checkpoint `.yml` file.\n\n```yml\n  - name: store_kada_validation_result\n    action:\n      class_name: KadaStoreValidationResultsAction\n      module_name: kada_ge_store_plugin.kada_store_validation\n      container: ${VALIDATIONS_CONTAINER}\n      prefix: lz/ge_landing/landing\n      connection_string: DefaultEndpointsProtocol=https;AccountName=${STORAGE_ACCOUNT_NAME};AccountKey=${STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net\n      account_url: ${SAS_URL}\n      access_key: ${SAS_TOKEN}\n```\n\nYou should change the prefix to your desired nested blob storage. Preference will be given to the `connection_string` as a connection method to the Azure storage account. If you are using storage access url and token, remove the `connection_string`. \n\n3. In your uncommited/config_variables.yml file or if you are using environment variables, add the following variables related to the azure storage account:\n\n    * VALIDATIONS_CONTAINER\n\n    Either:\n\n    * STORAGE_ACCOUNT_NAME\n    * STORAGE_ACCOUNT_KEY\n\n    Or:\n\n    * SAS_URL\n    * SAS_TOKEN\n    \n4. Add/Change the `run_name_template` in your checkpoint `.yml` file to `'%Y%m%d%H%M%S'`.\n\n### Note\n\nIf your checkpoint's `action_list` contains a `StoreValidationResultAction`, the validation results will get stored in the given validtions store inside `great_expectations.yml` file and also in the Azure Storage container with the custom `.json` filename. Basically, you'll be storing validation results in 2 different places.\n\nSince this is a new plugin, it might be worthwhile keeping the `StoreValidationResultAction` to make sure the validation results are getting stored even with a failure in this plugin.\n\n### Note\n\nAdded tags to facilitate version releasing and CI/CD operations\n",
    'author': 'Ali Bhayani',
    'author_email': 'ali@cloudshuttle.com.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
