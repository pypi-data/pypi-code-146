from setuptools import setup

with open("README.md","r") as f:
    long_description = f.read()

setup(
        name="pygrille",
        version="0.2.1",
        description="A quick way to write and visualise any code involving grids of squares in python.",
        py_modules=["pygrille","text"],
        package_dir={"":"src"},
        install_requires=["pygame",],
        long_description=long_description,
        long_description_content_type="text/markdown",
    )
