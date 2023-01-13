import setuptools

from lauterbach.trace32.rcl.version import __version__

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='lauterbach-trace32-rcl',
    version=__version__,
    author="Lauterbach GmbH",
    author_email="python-support@lauterbach.com",
    maintainer="Lauterbach GmbH",
    maintainer_email="python-support@lauterbach.com",
    description="Lauterbach TRACE32 Remote Control",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://www.lauterbach.com",
    packages=setuptools.find_packages(exclude=("*.internal*", "tests*")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
