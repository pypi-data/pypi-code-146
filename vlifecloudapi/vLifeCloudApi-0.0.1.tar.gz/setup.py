import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name = "vLifeCloudApi",
    version = "0.0.1",
    author = "Gopinath Muthusamy",
    author_email = "gopinathmu@virtusa.com",
    description = "vLife Support API for AWS Service",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    install_requires = [
        "boto3",
        "numpy"
    ]
)