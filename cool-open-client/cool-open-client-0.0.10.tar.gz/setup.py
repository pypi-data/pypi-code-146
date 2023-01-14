import pathlib
from setuptools import setup, find_packages

path_to_client = str(pathlib.Path(__file__).parent.absolute())

setup(
    name="cool-open-client",
    version="0.0.10",
    author="Shay Gus",
    author_email="sgusin@gmail.com",
    description="This library will enable the use of the CoolAutomation API by third party projects",
    long_description="file:README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/ShayGus/CoolControlOpenClient",
    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.9",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "certifi>= 14.05.14",
        "six >= 1.10",
        "python_dateutil >= 2.5.3",
        "urllib3 >= 1.15.1",
        "bidict >= 0.22.0",
        "rel >= 0.4.7",
        "websocket-client >= 1.3.3",
        "marshmallow >= 3.17.0",
        "marshmallow-dataclass >= 8.5.8",
        "typeguard >= 2.13.3",
        "aiohttp >= 3.8.1",
        "websockets >= 10.3",
    ],
)
