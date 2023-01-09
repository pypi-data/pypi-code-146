from setuptools import setup, find_packages
from viggofiscal._version import version

REQUIRED_PACKAGES = [
    'viggocore>=1.0.0,<2.0.0',
    'viggolocal>=1.0.0',
    'flask-cors'
]

setup(
    name="viggofiscal",
    version=version,
    summary='ViggoFiscal Module Framework',
    description="ViggoFiscal Backend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
