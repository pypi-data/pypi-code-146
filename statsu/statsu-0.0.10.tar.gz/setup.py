from setuptools import find_packages, setup

setup(
    name='statsu',
    version='0.0.10',
    description='Pandas Dataframe Editor',
    packages=find_packages(exclude=['statsu_test']),
    install_requires=[
        'PySide6',
        'pandas',
        'openpyxl',
    ],
    author='sbyim'
)