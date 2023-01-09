from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'shiftES',
    author = 'John C. Thomas',
    description='Implimentation of "A Robust Nonparametric Measure of Effect Size Based on an Analog of Cohens d...", '
                'R. Wilcox (2018). https://dx.doi.org/10.22237/jmasm/1551905677',
    author_email = 'jcthomas000@gmail.com',
    version='1.0.7',
    install_requires = ['numpy', 'pandas', 'openpyxl'],
    readme = "README.md",
    long_description=long_description,
    long_description_content_type='text/markdown', # required so pypi renders it right
    scripts = ['shiftES/shift_effectsize.py'],
    python_requires = '>=3.6',
    include_package_data=True, #uses MANIFEST.in
)
