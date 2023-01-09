import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConnectionManagementRPAOCI",
    version="0.0.3",
    author="Aravind Reddy Ravula",
    author_email="aravindreddyravula123@gmail.com",
    description="Test Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aravindreddyravula/ConnectionManagementRPAOCI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["ConnectionManagementRPAOCI"],
    include_package_data=True,
)
