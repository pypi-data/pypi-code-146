import setuptools


setuptools.setup(
    name="enhancer",
    version="0.4.4b0",
    author="Infinity",
    author_email="Newton@gmail.com",
    description="Made for me!",
    long_description="Never gonna give you up!",
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_namespace_packages(include=["safety.*"]),
    namespace_packages=["safety"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
