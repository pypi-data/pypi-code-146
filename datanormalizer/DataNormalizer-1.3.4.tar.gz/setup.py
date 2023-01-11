import setuptools
import DataNormalizer

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = [i.strip() for i in file if i.strip()]

def readme():
    with open("README.md") as f:
        return f.read()

setuptools.setup(
    name="DataNormalizer",
    description=DataNormalizer.__doc__,
    author=DataNormalizer.__author__,
    author_email=DataNormalizer.__email__,
    license=DataNormalizer.__license__,
    version=DataNormalizer.__version__,
    keywords="data DataNormalizer",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages = ['DataNormalizer'],
    install_requires=requirements
)