import setuptools
from yassm import config

install_requires = [
    "boto3 ~= 1.26.24",
    "click ~= 8.1.2",
    "PyYAML ~= 6.0",
]
setuptools.setup(
    name=config.CLI,
    description=config.NAME,
    long_description=f"{config.CLI} ({config.NAME}) is a tool for seeding AWS Secrets Manager secrets into local environment variables.",
    version=config.VERSION,
    packages=setuptools.find_packages(),
    install_requires=[
        "Click",
        "boto3",
        "PyYAML",
    ],
    entry_points=f"""
        [console_scripts]
        {config.CLI}={config.CLI}.main:cli
    """,
)
