import subprocess
import re
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

def get_version():
    regex = re.compile("__version__\s*\=\s*['\"](?P<version>.+?)['\"]")
    return regex.findall(open("flexmin/__init__.py").read())[0]

setup(
    name="flexmin",
    version=get_version(),
    url="",
    license="BSD",
    author="Richard Cooke",
    author_email="fm_1342@chrom3.co.uk",
    maintainer="Richard Cooke",
    maintainer_email="fm_1342@chrom3.co.uk",
    description="A flexible system admin web portal",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["flexmin", "flexmin.utils"],
    package_data={"flexmin": ["assets/*"],},
    install_requires=[
        "py4web>=1.20221110",
        "click",
        "pyyaml"
    ],
    entry_points={"console_scripts": ["flexmin=flexmin.flexmin_cli:cli"],},
    zip_safe=False,
    platforms="linux",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Systems Administration",
    ],
)
