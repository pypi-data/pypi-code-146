from setuptools import setup
from os import path


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name="pdfplumber-aemc",
    url="https://github.com/wargreymon28/pdfplumber-aemc",
    author="Jeremy Singer-Vine + Liew Chun Fui",
    author_email="wargreymon28@gmail.com",
    description="Plumb a PDF for detailed information about each char, rectangle, and line.",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="0.7.7",
    packages=['pdfplumber'],
    python_requires=">=3.7",
    install_requires=[
        'pdfminer.aemc==20221105',
        'Pillow>=9.1',
        'Wand>=0.6.10',
    ],
    entry_points={"console_scripts": ["pdfplumber = pdfplumber.cli:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
