import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="facts_gene",
    version="0.0.3",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="facts_gene for Networking Geeks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alias1978/facts_gene",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['pandas', 'numpy', 'xlrd', 'openpyxl', 'nettoolkit', 'capture_it']
)

