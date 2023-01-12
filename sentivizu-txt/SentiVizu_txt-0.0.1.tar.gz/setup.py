from setuptools import setup
from distutils.core import setup

setup(
    name='SentiVizu_txt',
    version='0.0.1',
    description='A sentiment analysis on text of different languages. Data visualization on sentiment analysis',
    author="JINKA THE AVIRAJ",
    author_email='jinkatheaviraj@gmail.com',
    py_modules=["SentiVizu_txt"],
    package_dir={"":"src"},
    install_requires=['matplotlib','googletrans==3.1.0a0','Translator','LANGUAGES'],
    inclide_package_data=True,
)