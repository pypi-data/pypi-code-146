from pathlib import Path
from setuptools import find_packages, setup

src = Path(__file__).parent

setup(
    name="pdxtra",
    version="1.0.0",
    description="Pandas with time-series data analysis in mind.",
    long_description=(src/"README.rst").read_text(),
    packages=find_packages(),
    install_requires=[
        "numpy>=1.22.3",
        "pandas>=1.4.2",
    ],
    python_requires=">=3.10.4",
    py_modules=["pdxtra"],
    license=(src/"LICENSE").read_text(),
    include_package_data=True,
)
