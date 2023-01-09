import setuptools

setuptools.setup(
    name="harbour",
    version="0.0.21",
    author="ebanx-dataops",
    author_email="dataops@ebanx.com",
    description="This project aims to make it easier to create images in AWS ECR. There are some implementations already in place like Dump tables from Mysql and Postgres databases.",
    url="https://github.com/ebanx/harbour",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["harbour = harbour.cli:cli"]},
    install_requires=[
        "click==7.0",
        "requests==2.22.0",
        "boto3==1.11.9",
        "structlog==20.1.0",
        "PyMySQL==0.9.3",
        "psycopg2-binary==2.9.5",
    ],
    extras_require={
        "test": [],
        "build": [
            "twine",
        ],
    },
)
