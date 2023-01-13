from setuptools import setup, find_packages

setup(
    name='aaki',
    version='0.3.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['spacy', 'pytest'],
)