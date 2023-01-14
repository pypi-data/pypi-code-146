# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdk_pynamodb']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk-lib>=2.60.0,<3.0.0', 'pynamodb>=5.3.4,<6.0.0']

setup_kwargs = {
    'name': 'cdk-pynamodb',
    'version': '0.1.0',
    'description': '',
    'long_description': '============\nCDK PynamoDB\n============\n\nAWS CDK Construct for DynamoDB Table from PynamoDB Model.\n\nStreamline DynamoDB create and deploy with PynamoDB and AWS CDK.\n\nThis package provides a construct for creating a DynamoDB table using the AWS CDK and PynamoDB models.\nIt simplifies the process of creating and deploying DynamoDB tables in your AWS environment.\n\nDefine your tables in a reusable and predictable way with infrastructure-as-code.\n\n\nInstallation\n============\nFrom PyPi::\n\n    $ pip install cdk-pynamodb\n\nFrom GitHub::\n\n    $ pip install git+https://github.com/altoria/cdk-pynamoDB#egg=cdk-pynamodb\n\n\n\nBasic Usage\n===========\n\nCreate a model that describes your DynamoDB table.\n\n.. code-block:: python3\n\n    from pynamodb.models import Model\n\n    class UserTable(Model):\n        class Meta:\n            host = "http://localhost:8000"\n            table_name = "user-table"\n            billing_mode = PROVISIONED_BILLING_MODE\n            read_capacity_units = 10\n            write_capacity_units = 3\n\n        user_id = UnicodeAttribute(hash_key=True)\n        email = UnicodeAttribute(null=True)\n\nNow, you can import and construct model in AWS CDK\n\n.. code-block:: python3\n\n    from models import UserTable\n\n    from aws_cdk import Stack\n    from constructs import Construct\n\n    class Database(Stack):\n        def __init__(self, scope: Construct, id_: str):\n            super().__init__(scope, id_)\n\n            self.table = PynamoDBTable.from_pynamodb_model(self, pynamodb_model=UserTable)\n',
    'author': 'SeongHun Kim',
    'author_email': 'alto@pendragon.kr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
