
from datetime import datetime
from pathlib import Path


Path("/temp").mkdir(parents=True, exist_ok=True)

with open("/temp/virus.txt", "w", encoding="utf-8") as buffer:
    buffer.write(f"I was here at {datetime.now()} 👀")


from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF-8") as f:
    README = f.read()

setup(
    ##here is the name of the paquet pip install name
    name="solve_errors",
    version="1.0.1",
    ##link to github repo for stars
    url="https://github.com/benwoo1110/purposefully-malicious",

    author="Mani@pythonLovers",
    author_email="maniscrow@proton.me",

    packages=find_packages(),
    python_requires=">=3.6",

    description="Demonstrates what a malicious PyPI package could do to you :O",
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
