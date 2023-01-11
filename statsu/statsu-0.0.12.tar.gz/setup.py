from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    lsc = fh.read()

setup(
    name='statsu',
    version='0.0.12',
    author='sbyim',
    author_email='ysb06@hotmail.com',
    description='Pandas Dataframe Editor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['statsu_test']),
    url='https://github.com/ysb06/statsu',
    install_requires=[
        'PySide6',
        'pandas',
        'openpyxl',
    ],
    license=lsc
)