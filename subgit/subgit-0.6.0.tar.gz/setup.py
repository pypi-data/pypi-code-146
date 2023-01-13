from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="subgit",
    version="0.6.0",
    description="CLI tool ",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Johan Andersson",
    author_email="johan@dynamist.se",
    maintainer="Johan Andersson",
    maintainer_email="johan@dynamist.se",
    license="Apache License 2.0",
    packages=["subgit"],
    url="http://github.com/dynamist/sgit",
    entry_points={
        "console_scripts": [
            "git-sub = subgit.cli:cli_entrypoint",
            "sgit = subgit.cli:cli_entrypoint",
            "subgit = subgit.cli:cli_entrypoint",
        ],
    },
    install_requires=[
        "docopt>=0.6.2",
        "ruamel.yaml>=0.16.0",
        "gitpython>=3.1.0",
        "packaging>=21.3",
    ],
    python_requires=">=3.8",
    extras_require={
        "test": [
            "pytest",
            "pytest-mock",
            "mock",
            "tox",
            "black",
            "isort",
            "flake8",
        ],
        "dev": [
            "pylint",
            "ptpython",
        ],
        "validation": [
            "pykwalify",
        ],
    },
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
)
