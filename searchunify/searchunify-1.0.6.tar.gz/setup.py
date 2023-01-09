#!/usr/bin/env python

import setuptools

setuptools.setup(
    include_package_data=True,
    name="searchunify",
    version='1.0.6',
    description='The SearchUnify SDK enables developers to easily work with the SearchUnify platform and build scalable solutions with search, analytics, crawlers and more.',
    author='SearchUnify',
    author_email='ankur.mahajan@grazitti.com',
    url='https://www.searchunify.com/',
    packages=[
        'searchunify',
        'searchunify.core',
        'searchunify.core.analytics',
        'searchunify.core.auth',
        'searchunify.core.content',
        'searchunify.core.search',
        'searchunify.client', 
        'searchunify.utils',
        'searchunify.utils.apis',
        'searchunify.utils.constants',
        'searchunify.utils.http_client',
        'searchunify.utils.validation'
    ],
    install_requires=['requests==2.23.0', 'schema==0.7.4']
)