from setuptools import setup
from setuptools import find_packages

version_py = "ExpreLev/_version.py"
exec(open(version_py).read())

setup(
    name="ExpreLev", # Replace with your own username
    version=__version__,
    author="Benxia Hu",
    author_email="hubenxia@gmail.com",
    description="TPM/CPM/FPKM analysis",
    long_description="analyze TPM/CPM/FPKM",
    url="https://pypi.org/project/ExpreLev/",
    entry_points = {
        "console_scripts": ['ExpreLevGene = ExpreLev.ExpreLevGene:main',
                            'ExpreLevExon = ExpreLev.ExpreLevExon:main',
                            'ExpreLevEpi = ExpreLev.ExpreLevEpi:main',]
        },
    python_requires = '>=3.6',
    packages = ['ExpreLev'],
    install_requires = [
        'numpy',
        'pandas',
        'argparse',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    zip_safe = False,
  )