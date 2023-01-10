from setuptools import setup, find_packages

VERSION= '0.0.16'
DESCREIPTION='AWS Database Connection Handler'
LONG_DESCRIPTION='Handles connecting to databases within the AWS environment'
NAME='Connection Handler'
AUTHOR='Tyler Arnold'
AUTHOR_EMAIL='tarnold@databankimx.com'


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCREIPTION,
    packages=find_packages(exclude=["psycopg2"]),
    keywords=['Python', 'AWS', 'Database']
)