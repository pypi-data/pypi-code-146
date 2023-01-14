from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A lib of random generator, games and calculator'
LONG_DESCRIPTION = 'This library consist of 3 packages general, calculator and game. In general we have a generator module in which we can have random dice value, madlibs, password and a timer module. In calculator we can calculate area of shapes and basic addition subtraction and division etc. Lastly in games we can play a number guessing game'

# Setting up
setup(
    name="rand_calc_guess",
    version=VERSION,
    author="Anoosha Tanseer",
    author_email="atanseer2016@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'random', 'timer', 'area', 'game','guess','madlib','countdown','addition','mod','password','shape'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)