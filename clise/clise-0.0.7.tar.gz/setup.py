import setuptools
import re

author = "Jaesub Hong"
name   = "clise"

with open("README.txt", "r") as fh:
    long_description = fh.read()

mat=re.search('ver ([0-9.]+) by', long_description)
if not bool(mat): 
    print('cannot find the version number, exiting...')
    exit()

version = mat.group(1)


with open(name+"/__init__.py", "w") as fi:
	fi.write('__version__ = "'+version+'"\n')
	fi.write('__author__  = "'+author+'"')

setuptools.setup(
    name		     = name, 
    version		     = version,
    author		     = author, 
    author_email	 = "jhong@cfa.harvard.edu",
    packages	     = [name],
    url		         = "https://pypi.org/project/"+name+'/'+version,

    description	     = "Command liner with JSON based input file",
    long_description = long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
		'textwrap3'
	    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            name+'=clise.heron:main',
        ],
    },
)
