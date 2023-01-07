import os
from setuptools import find_packages, setup

# Constants
PACKAGE_NAME = "valcheck"
PACKAGE_VERSION = "0.2.7"
AUTHOR_NAME = "Nishant Rao"
AUTHOR_EMAIL_ID = "nishant.rao173@gmail.com"
FILEPATH_TO_README = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
FILEPATH_TO_REQUIREMENTS = os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")
REPOSITORY_URL = "https://github.com/Nishant173/valcheck"

# Requirements
install_requires = []
with open(file=FILEPATH_TO_REQUIREMENTS, mode="r") as fp:
    install_requires.extend(
        [s for s in [line.strip(" \n") for line in fp] if not s.startswith("#") and s != ""]
    )

# Setup
setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description="Package for quick data validation (in Python)",
    long_description=f"Package for quick data validation (in Python). Our repository: {REPOSITORY_URL}",
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL_ID,
    url=REPOSITORY_URL,
    packages=find_packages(where="."),
    include_package_data=True,
    install_requires=install_requires,
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)

