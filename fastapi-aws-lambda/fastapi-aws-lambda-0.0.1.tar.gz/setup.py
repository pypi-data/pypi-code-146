from setuptools import setup, find_packages

setup(
    name="fastapi-aws-lambda",
    version="0.0.1",
    description="A Wrapper for FastAPI to run on AWS Lambda",
    long_description="A Wrapper for FastAPI to run on AWS Lambda",
    long_description_content_type="text/markdown",
    url="https://github.com/obahamonde/fastapi_lambda",
    author="Oscar Bahamonde",
    author_email="oscar.bahamonde@hatarini.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "odmantic",
        "pydantic[email,dotenv]",
        "python-multipart",
        "python-jose",
        "mangum"
    ]
)