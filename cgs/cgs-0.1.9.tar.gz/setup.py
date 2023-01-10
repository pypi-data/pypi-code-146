from setuptools import setup
import os, re

with open("README.md", "r") as f:
    long_desc = f.read()

# with open("requirements.txt", "r") as f:
#     requirements = [line.rstrip() for line in f]

requirements = [
    "beautifulsoup4>=4.10.0",
    "certifi>=2021.10.8",
    "charset-normalizer>=2.0.12",
    "idna>=3.3",
    "requests>=2.27.1",
    "soupsieve>=2.3.1",
    "urllib3>=1.26.8"
]

SRC = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(os.path.join(SRC, 'cgs/__init__.py')) as f:
        for line in f:
            m = re.match("__version__ = \"(.*)\"", line)
            if m:
                return m.group(1)
    raise SystemExit("Could not find version string.")

setup(
    name='cgs',
    version=get_version(),
    packages=['cgs'],
    author='msa360',
    url="https://github.com/Msa360/cgs-csfoy-gym",
    license='MIT',
    description="Create & update reservations at Cégep Sainte-Foy gym with this simple api.",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    author_email='arnaud25@icloud.com',
    entry_points={'console_scripts': ['cgs=cgs.cli:cli']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License'
    ]
)