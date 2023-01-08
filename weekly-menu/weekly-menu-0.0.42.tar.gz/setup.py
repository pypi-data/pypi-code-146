import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weekly-menu",
    version="0.0.42",
    author="Andrea Cioni",
    description="Automate your weekly menu with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreacioni/weekly-menu",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
