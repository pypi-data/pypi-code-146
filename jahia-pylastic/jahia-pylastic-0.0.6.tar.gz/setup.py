import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jahia-pylastic",
    version="0.0.6",
    author="Laurent Fuentes",
    maintainer="Jahia",
    maintainer_email="paas@jahia.com",
    description="Interact with Jelastic API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jahia/pylastic",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
