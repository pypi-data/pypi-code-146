# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name="django-passwordless",
    version="1.0.3",
    author="Jon Combe",
    author_email="me@joncombe.net",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    license="MIT licence, see LICENCE file",
    description="Secure passwordless login for Django",
    long_description="View readme on github: https://github.com/joncombe/django-passwordless",
    url="https://github.com/joncombe/django-passwordless",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False,
)
