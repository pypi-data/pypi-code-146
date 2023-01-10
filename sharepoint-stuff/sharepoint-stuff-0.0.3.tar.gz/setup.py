from setuptools import setup

VERSION = '0.0.3'
DESCRIPTION = 'Package that adds a range of functionality for working with sharepoint sites - under constant development'

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="sharepoint-stuff",
    url="https://github.com/george-oconnor/sharepoint-stuff",
    version=VERSION,
    author="george.oconnor (George O' Connor)",
    author_email="<george@georgestools.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["sharepoint_stuff"],
    package_dir={'': 'src'},
    install_requires=["Office365-REST-Python-Client", "office365"],
    keywords=['python', 'sharepoint', 'upload', 'sharepoint site', 'download', 'office', 'office365', 'microsoft', 'microsoft365', 'azure', 'site'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)