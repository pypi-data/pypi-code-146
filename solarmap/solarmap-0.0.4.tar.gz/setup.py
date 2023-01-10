from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'Get HEE Coordinates for spacecraft around the Sun'
LONG_DESCRIPTION = 'A package that allows to get coordinates and plot different spacecraft around the Sun given a certain date.'

# Setting up
setup(
    name="solarmap",
    version=VERSION,
    author="Luis Alberto Canizares",
    author_email="<canizares@cp.dias.ie>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['sunpy', 'astropy', 'astroquery'],
    keywords=['python', 'solar', 'nasa', 'esa', 'spacecraft', 'coordinates', 'sun', 'corona', 'parker', 'solar orbiter'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)