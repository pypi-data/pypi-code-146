# coding: utf-8

"""
    zadara api

    zadarapyV2 operations

"""


from setuptools import setup, find_packages  # noqa: H301


NAME = "zadarapyV2"
VERSION = "v22.09" 
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23"
]
    

setup(
    name=NAME,
    version=VERSION,
    description="zadara api",
    author_email="harel.feldman@zadarastorage.com",
    url="https://github.com/zadarastorage/zadara-clients/tree/master/zadarapyV2",
    keywords=["zadarapy"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description="""\
    Python client for ZADARA storage components:
    Vpsa, Commandcenter, ProvisioningPortal and Zios
    """
)
