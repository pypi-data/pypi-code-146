from setuptools import setup, find_packages

setup(
    name='IneryPy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'base58',
        'ecdsa',
        'regex',
        'pytz',
        'six',
        'colander',
        'ordereddict',
    ],
    url='https://github.com/pnkg99/IneryPy.git',
    license='MIT',
    author='Petar N',
    author_email='pnkg99@example.com',
    description='A package for RPC communication with Inery blockchain'
)