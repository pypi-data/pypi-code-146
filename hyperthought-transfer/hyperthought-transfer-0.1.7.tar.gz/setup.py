"""
    Setup file for hyperthought-transfer.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.2.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup, find_packages


if __name__ == "__main__":
    try:
        setup(
            version="0.1.7",
            use_scm_version={
                "version_scheme": "no-guess-dev",
                "local-scheme": "no-local-version",
            },
            packages=find_packages(where="src"),
            package_dir={"": "src"},
            include_package_data=True,
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
