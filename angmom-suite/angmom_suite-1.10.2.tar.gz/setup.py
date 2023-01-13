import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# DO NOT EDIT THIS NUMBER!
# IT IS AUTOMATICALLY CHANGED BY python-semantic-release
__version__ = "1.10.2"

setuptools.setup(
    name="angmom_suite",
    version=__version__,
    author="Chilton Group",
    author_email="nicholas.chilton@manchester.ac.uk",
    description="A package for working with phenomenological spin and angular momentum operators", # noqa
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/chilton-group/angmom_suite",
    project_urls={
        "Bug Tracker": "https://gitlab.com/chilton-group/angmom_suite/issues",
        "Documentation": "https://chilton-group.gitlab.io/angmom_suite"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"."},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["numpy", "scipy>=1.7.0", "sympy", "matplotlib", "h5py",
                      "hpc_suite>=1.2.0", "molcas_suite>=1.11.0"]

)
