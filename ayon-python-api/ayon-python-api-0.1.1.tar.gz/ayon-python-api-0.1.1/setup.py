import os
from setuptools import setup

current_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_dir, "README.md")
with open(readme_path, "r") as stream:
    long_description = stream.read()

version_path = os.path.join(current_dir, "ayon_api", "version.py")
version_content = {}
with open(version_path, "r") as stream:
    exec(stream.read(), version_content)
package_version = version_content["__version__"]


setup(
    name="ayon-python-api",
    version=package_version,
    py_modules=["ayon_api"],
    package_dir={"": "ayon_api"},
    author="ynput.io",
    author_email="info@ynput.io",
    description="Ayon Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ynput/ayon-python-api",
    include_package_data=True,
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "requests >= 2.28.1",
        "six >= 1.15",
    ],
    keywords=["ayon", "ynput", "OpenPype", "vfx"]
)