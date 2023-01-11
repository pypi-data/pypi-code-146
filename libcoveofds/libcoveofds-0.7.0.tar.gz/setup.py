from setuptools import find_packages, setup

setup(
    name="libcoveofds",
    version="0.7.0",
    author="Open Data Services",
    author_email="code@opendataservices.coop",
    url="https://github.com/Open-Telecoms-Data/lib-cove-ofds",
    project_urls={
        "Documentation": "https://libcoveofds.readthedocs.io/en/latest/",
        "Issues": "https://github.com/Open-Telecoms-Data/lib-cove-ofds/issues",
        "Source": "https://github.com/Open-Telecoms-Data/lib-cove-ofds",
    },
    description="A data review library",
    packages=find_packages(),
    long_description="A data review library",
    python_requires=">=3.8",
    install_requires=[
        "jsonschema",
        "requests",
        "jsonref",
        "json-merge-patch",
        "rfc3987",
    ],
    extras_require={
        "dev": ["pytest", "flake8", "black==22.3.0", "isort", "mypy", "Sphinx"]
    },
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    entry_points="""[console_scripts]
libcoveofds = libcoveofds.cli:main""",
    include_package_data=True,
)
