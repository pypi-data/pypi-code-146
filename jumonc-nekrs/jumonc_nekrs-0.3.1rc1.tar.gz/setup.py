import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="jumonc_nekrs",
    version="0.3.1rc1",
    install_requires=["JuMonC>=0.10.0rc3", "pluggy"],
    entry_points={
        "jumonc": [
            "nekrs = jumonc_nekrs.jumonc_nekrs_plugin",
        ]
    },
    description="LogParser jumonc plugin for nekRS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.jsc.fz-juelich.de/coec/jumonc_nekrs",
    author="Christian Witzler",
    author_email="c.witzler@fz-juelich.de",
    packages=["jumonc_nekrs"],
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
)
