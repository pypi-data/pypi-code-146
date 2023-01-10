from setuptools import setup
from pathlib import Path

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='unavoids',
    version='1.4',    
    short_description='UNAVOIDS: Unsupervised and Nonparametric Approach for Visualizing Outliers and Invariant Detection Scoring',

    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/isotlaboratory/UNAVOIDS-Code',
    author='Yousef, Waleed A. and Traoré, Issa and Briguglio, William',
    author_email='wyousef@uvic.ca',
    license='GNU GENERAL PUBLIC LICENSE',
    packages=['unavoids'],
    install_requires=[],

    classifiers=[
    ],
)