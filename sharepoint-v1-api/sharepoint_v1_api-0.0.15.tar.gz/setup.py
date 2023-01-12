from setuptools import setup

__version__ = "0.0.15"

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

packages = ["sharepoint_api"]

setup(
    name="sharepoint_v1_api",
    version=__version__,
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aske Bluhme Klok",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="Sharepoint",
    packages=packages,
    install_requires=["requests", "requests-ntlm"],
    python_requires=">=3.6.8"
)
