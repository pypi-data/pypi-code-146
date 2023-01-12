import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="qbeast-cli",
    version="0.2.0",
    author="Qbeast",
    description="A command line interface for the Qbeast services",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "qbeast = qbeast.main:cli",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["click==8.1.3", "requests==2.27.1", "tabulate==0.9.0", "PyYAML==6.0"],
)
