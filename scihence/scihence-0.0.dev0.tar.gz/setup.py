"""Sets up the package."""

import re
from pathlib import Path

from setuptools import find_packages, setup


def get_string_from_file_by_variable_name(obj_name: str, file_path: str) -> str:
    """Get a string from the source code of a file by its variable name.

    :param obj_name: Variable name of the string defined in the file
    :type obj_name: str
    :param file_path: Path to the file
    :type file_path: str
    :return: Variable name value
    :rtype: str
    """
    with open(file_path, encoding="utf-8") as file:
        file = file.read()
    result = re.search(rf'{obj_name}\s*=\s*[\'"]([^\'"]*)[\'"]', file)
    return result.group(1)


name = "scihence"

package_data = {
    name: [
        "py.typed",
        "visualise/noto/**",
        "visualise/mplstyles/*",
    ],
}

install_requires = [
    "matplotlib>=3.5.0",
    "Pillow>=7.0.0",
    "plotly>=5.0.0",
    "pandas>=1.3.0",
]

extras_require = {
    "dev": [
        "black>=22.6.0",
        "flake8>=5.0.4",
        "flake8-docstrings>=1.6.0",
        "isort>=5.10.1",
        "jupytext>=1.14.1",
        "mypy>=0.971",
        "pipreqsnb>=0.2.4",
        "pre-commit>=2.20.0",
        "pytest>=7.1.2",
        "pytest-cov>=3.0.0",
        "toml>=0.10.2",
        "tox>=3.25.0",
        "twine>=4.0.2",
    ],
}

setup(
    name=name,
    author="Henry Broomfield",
    description="Henry's tools in Python.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data=package_data,
    install_requires=install_requires,
    python_requires=">=3.10.0",
    extras_require=extras_require,
    url="https://gitlab.com/HennersBro98/scihence",
    license=(Path(__file__).parent / "LICENSE").read_text(),
    version=get_string_from_file_by_variable_name("__version__", f"src/{name}/__init__.py"),
)
