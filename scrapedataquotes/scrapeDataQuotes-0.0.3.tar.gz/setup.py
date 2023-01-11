from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scrapeDataQuotes',
    version='0.0.3',
    description='HMTV live news scraping',
    author= 'Phani Siginamsetty',
    # url = 'https://github.com/funnyPhani/Test_repo_rlms',
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=["web scraping"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['scrapeDataQuotes'],
    package_dir={'':'src'},
    install_requires = [
       "pandas",
       "requests",
       "bs4"

    ]
)