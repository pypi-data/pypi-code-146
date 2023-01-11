import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="retirement",
    version="0.1.3",
    author="Example Author",
    author_email="author@example.com",
    description="retirement calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pstrito/RetirementPip.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
