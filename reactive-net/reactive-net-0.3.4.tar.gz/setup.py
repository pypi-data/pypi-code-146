import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reactive-net",
    version="0.3.4",
    author="Gianluca Scopelliti",
    author_email="gianlu.1033@gmail.com",
    description="Networking library for reactive-tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AuthenticExecution/reactive-net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
