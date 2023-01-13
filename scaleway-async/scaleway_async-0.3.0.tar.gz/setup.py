# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scaleway_async',
 'scaleway_async.account',
 'scaleway_async.account.v2',
 'scaleway_async.applesilicon',
 'scaleway_async.applesilicon.v1alpha1',
 'scaleway_async.baremetal',
 'scaleway_async.baremetal.v1',
 'scaleway_async.container',
 'scaleway_async.container.v1beta1',
 'scaleway_async.domain',
 'scaleway_async.domain.v2beta1',
 'scaleway_async.flexibleip',
 'scaleway_async.flexibleip.v1alpha1',
 'scaleway_async.function',
 'scaleway_async.function.v1beta1',
 'scaleway_async.iam',
 'scaleway_async.iam.v1alpha1',
 'scaleway_async.instance',
 'scaleway_async.instance.v1',
 'scaleway_async.iot',
 'scaleway_async.iot.v1',
 'scaleway_async.k8s',
 'scaleway_async.k8s.v1',
 'scaleway_async.lb',
 'scaleway_async.lb.v1',
 'scaleway_async.marketplace',
 'scaleway_async.marketplace.v1',
 'scaleway_async.marketplace.v2',
 'scaleway_async.mnq',
 'scaleway_async.mnq.v1alpha1',
 'scaleway_async.rdb',
 'scaleway_async.rdb.v1',
 'scaleway_async.redis',
 'scaleway_async.redis.v1',
 'scaleway_async.registry',
 'scaleway_async.registry.v1',
 'scaleway_async.tem',
 'scaleway_async.tem.v1alpha1',
 'scaleway_async.test',
 'scaleway_async.test.v1',
 'scaleway_async.vpc',
 'scaleway_async.vpc.v1',
 'scaleway_async.vpcgw',
 'scaleway_async.vpcgw.v1']

package_data = \
{'': ['*']}

install_requires = \
['scaleway-core>=0,<1']

setup_kwargs = {
    'name': 'scaleway-async',
    'version': '0.3.0',
    'description': 'Scaleway SDK for Python',
    'long_description': '# Scaleway Python SDK - Async\n',
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
