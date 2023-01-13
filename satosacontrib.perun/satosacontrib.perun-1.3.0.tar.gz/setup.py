from setuptools import setup, find_packages

setup(
    name="satosacontrib.perun",
    python_requires=">=3.9",
    url="https://github.com/CESNET/satosacontrib.perun.git",
    description="Module with satosa micro_services",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "SATOSA~=8.1",
        "pysaml2~=7.1",
        "requests~=2.28",
        "perun.connector~=3.3",
        "PyYAML~=6.0",
        "SQLAlchemy~=1.4",
        "jwcrypto~=1.3",
        "natsort~=8.2.0",
        "python-dateutil~=2.8",
        "geoip2~=4.6",
        "user_agents~=2.2",
    ],
    extras_require={
        "curl": ["pycurl~=7.45"],
    },
)
