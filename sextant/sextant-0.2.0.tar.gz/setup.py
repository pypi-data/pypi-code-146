"""
Package configuration.


SPDX-License-Identifier: GPL-3.0-or-later
"""

from setuptools import find_packages, setup

install_requires = []

# Extra dependencies
extras_require = {
    # Test dependencies
    "tests": ["flake8>=3.2.1", "pytest>=6.1.0", "black>=22.0.0"],
}

setup_requires = [
    "setuptools_scm>=1.15.0",
]

setup(
    author="Giuseppe Lavagetto",
    author_email="joe@wikimedia.org",
    description="CLI tool to work with helm charts and our helm chart modules.",
    extras_require=extras_require,
    install_requires=install_requires,
    keywords=["wmf", "automation", "kubernetes", "helm", "charts"],
    license="GPLv3+",
    name="sextant",
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    platforms=["GNU/Linux"],
    setup_requires=setup_requires,
    use_scm_version=True,
    url="https://gitlab.wikimedia.org/repos/sre/sextant",
    zip_safe=False,
    entry_points={"console_scripts": ["sextant = sextant.cli:main"]},
)
