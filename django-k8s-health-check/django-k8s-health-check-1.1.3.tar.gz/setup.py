# -*- coding: utf-8 -*-
#!/usr/bin/env python
from io import open

from setuptools import find_packages, setup

from django_k8s_health_check import __version__

extras_require = {
    'dev': [
        'autopep8',
    ],
    'code-quality': [
        'isort',
        'bandit',
        'xenon',
    ]
}


setup(
    name='django-k8s-health-check',
    version=__version__,
    description='Django Health Check',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Shinneider Libanio da Silva',
    author_email='shinneider-libanio@hotmail.com',
    url='https://github.com/shinneider/django-k8s-health-check',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    python_requires=">=3.3",
    install_requires=[
        'django',
        'djangorestframework'
    ],
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
