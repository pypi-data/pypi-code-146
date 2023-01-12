import setuptools
from pathlib import Path

__version__ = "0.0.3"

ROOT_DIR = Path(".")

with open("requirements.txt") as f:
    requirements = f.readlines()

with open(str(ROOT_DIR / "README.md")) as readme:
    description = readme.read()

setuptools.setup(
    name="kepingai-sdk",
    packages=[
        "kepingai"
    ],
    version=__version__,
    author="PT. Idabagus Engineering Indonesia",
    author_email="support@kepingai.com",
    maintainer="Ida Bagus Ratu Diaz Agasatya",
    maintainer_email="diazagasatya@kepingai.com",
    description=description,
    install_requires=requirements,
    python_requires=">=3.7"
)
