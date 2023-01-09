import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="korcount", # Replace with your own username
    version="0.0.1",
    author="binjang",
    author_email="bjang98@gmail.com",
    description="A package for korean number strings to integer values ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/korcount",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)