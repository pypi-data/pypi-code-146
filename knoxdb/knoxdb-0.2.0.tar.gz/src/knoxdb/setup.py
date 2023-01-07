from setuptools import find_packages, setup

setup(
    name='knoxdb',
    packages=find_packages(include=['knoxdb']),
    version='0.2.0',
    description='Quickly create a PostgresSQL DB without the hassle.',
    author='Knox Dobbins',
    license='MIT',
)