# we are creating our won pacakgae to publish on piPy
import setuptools
from pathlib import Path
setuptools.setup(
    name="munazzatsd",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])

)
