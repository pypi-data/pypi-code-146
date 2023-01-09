#!/usr/bin/env python3
"""Install coop"""

from setuptools import find_packages, setup

with open("coop/_version.py", "r") as f:
    version = None
    exec(f.read())

with open("README.rst", "r") as f:
    readme = f.read()


install_requires = ["wagtail>=3.0"]

setup(
    name="coop",
    version=version,
    description="Standard base to build Wagtail sites from",
    long_description=readme,
    author="Neon Jungle",
    author_email="developers@neonjungle.studio",
    url="https://gitlab.com/neonjungle/coop",
    install_requires=[
        "wagtail~=4.1.0",
        "django>=3.2,<=4.0",
        "psycopg2-binary~=2.9.0",
        "pytz>=0",
        "Jinja2~=3.1.0",
        "django-honeypot~=1.0.0",
        "django-webpack-loader~=1.8.0",
        "wagtail-metadata~=4.0.0",
        "wagtailfontawesome~=1.0",
        "wagtail-icomoon",
        "bugsnag~=4.0",
        "wagtail-cache~=2.2.0",
        "wagtail-factories~=4.0.0",
    ],
    extras_require={
        "all": [
            "mailchimp3~=3.0.0",
            "diskcache~=5.2.0",
        ],
        "cache": ["diskcache~=5.2.0"],
        "mailchimp": ["mailchimp3~=3.0.0"],
    },
    zip_safe=False,
    license="BSD License",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    package_data={},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
    ],
)
