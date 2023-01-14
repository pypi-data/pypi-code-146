from setuptools import setup
from setuptools import find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name="divide-char-type",
    version="0.1.6",
    py_modules=["divide_char_type"],
    install_requires=[],

    # metadata to display on PyPI
    author="Shinya Akagi",
    description="Divide documents by character type",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/ShinyaAkagiI/divide_character_type", 
    license="PSF",
)
