
from datetime import datetime
from pathlib import Path


Path("/temp").mkdir(parents=True, exist_ok=True)
with open("/temp/virus.txt", "w", encoding="utf-8") as buffer:
    buffer.write(f"I was here at {datetime.now()} 👀")



###parameter_setup
from setuptools import setup, find_packages
with open("README.md", "r", encoding="UTF-8") as f:
    README = f.read()

setup(
    ##here is the name of the paquet pip install name
    name="solve_errors",
    version='1.0.3',
    url="https://github.com/pypa/pip",

    author="Mani@pythonLovers",
    author_email="maniscrow@proton.me",

    packages=find_packages(),
    python_requires=">=3.6",

    description="An automated package that solves basic python errors",
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
