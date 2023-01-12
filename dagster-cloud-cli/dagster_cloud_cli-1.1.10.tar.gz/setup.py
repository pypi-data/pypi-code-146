from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "dagster_cloud_cli/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


setup(
    name="dagster_cloud_cli",
    version=get_version(),
    author_email="hello@elementl.com",
    packages=find_packages(exclude=["dagster_cloud.cli_tests*"]),
    include_package_data=True,
    install_requires=[
        # packaging v22 has build compatibility issues with dbt as of 2022-12-07
        # upper bound can be removed as soon as BK passes with packaging >=22
        "packaging>=20.9,<22",
        "questionary",
        "requests",
        "typer[all]>=0.4.1",
        "PyYAML>=5.1",
    ],
    extras_require={},
    author="Elementl",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dagster-cloud = dagster_cloud_cli.entrypoint:app",
        ]
    },
)
