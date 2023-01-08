from setuptools import setup

setup(
    name="conventional_with_data",
    version="0.1.0",
    py_modules=["cz_conventional_with_data"],
    license="MIT",
    description="Extend the Commitizen Conventional-Commits implementation to allow `data:` in the commit message.",
    install_requires=["commitizen"],
)
