import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyReporter",
    version="1.0.10",
    author="Alex Au",
    author_email="AlexXianZhenYuAu@gmail.com",
    description="A Python reporting API that helps with reading and writing tabular data in Excel, SQl, etc...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex-Au1/PyReporter",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "holidays",
        "numpy",
        "office365",
        "Office365_REST_Python_Client",
        "openpyxl",
        "pandas",
        "pyodbc",
        "requests",
        "selenium",
        "setuptools",
        "SharePlum"
    ],
    python_requires='>=3.6',
)
