from setuptools import setup

setup(
    name="the-spymaster-util",
    version="1.16.2",
    description="Common utilities and infra for The Spymaster game.",
    author="Asaf Kali",
    author_email="akali93@gmail.com",
    url="https://github.com/asaf-kali/the-spymaster-util",
    install_requires=[
        "pydantic~=1.9",
        "dynaconf~=3.1",
        "boto3~=1.24",
        "ulid-py~=1.1",
        "requests~=2.28",
    ],
    include_package_data=True,
)
