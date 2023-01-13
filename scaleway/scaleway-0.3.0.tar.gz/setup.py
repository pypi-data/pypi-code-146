# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scaleway',
 'scaleway.account',
 'scaleway.account.v2',
 'scaleway.applesilicon',
 'scaleway.applesilicon.v1alpha1',
 'scaleway.baremetal',
 'scaleway.baremetal.v1',
 'scaleway.container',
 'scaleway.container.v1beta1',
 'scaleway.domain',
 'scaleway.domain.v2beta1',
 'scaleway.flexibleip',
 'scaleway.flexibleip.v1alpha1',
 'scaleway.function',
 'scaleway.function.v1beta1',
 'scaleway.iam',
 'scaleway.iam.v1alpha1',
 'scaleway.instance',
 'scaleway.instance.v1',
 'scaleway.iot',
 'scaleway.iot.v1',
 'scaleway.k8s',
 'scaleway.k8s.v1',
 'scaleway.lb',
 'scaleway.lb.v1',
 'scaleway.marketplace',
 'scaleway.marketplace.v1',
 'scaleway.marketplace.v2',
 'scaleway.mnq',
 'scaleway.mnq.v1alpha1',
 'scaleway.rdb',
 'scaleway.rdb.v1',
 'scaleway.redis',
 'scaleway.redis.v1',
 'scaleway.registry',
 'scaleway.registry.v1',
 'scaleway.tem',
 'scaleway.tem.v1alpha1',
 'scaleway.test',
 'scaleway.test.v1',
 'scaleway.vpc',
 'scaleway.vpc.v1',
 'scaleway.vpcgw',
 'scaleway.vpcgw.v1']

package_data = \
{'': ['*']}

install_requires = \
['scaleway-core>=0,<1']

setup_kwargs = {
    'name': 'scaleway',
    'version': '0.3.0',
    'description': 'Scaleway SDK for Python',
    'long_description': '# Scaleway Python SDK\n\nThis SDK enables you to interact with Scaleway APIs.\n',
    'author': 'Scaleway',
    'author_email': 'opensource@scaleway.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
