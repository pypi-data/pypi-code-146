from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alice-api",
    version="1.0.0",
    description="Alice api its come with sms spammer, truewallet system and host system!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alice-api/alice-api",
    author="pipatpong",
    author_email="kanyatit2500@gmail.com",
    license="MIT",
    packages=["alice_api"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "flask",
        "requests",
        "datetime",
        "os"
    ],
)
