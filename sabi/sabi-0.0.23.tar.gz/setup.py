from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="sabi",
    version="0.0.23",
    description="A client for the SABI api (www.sabi.ai)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sabi-ai/sabi",  # Optional
    author="Scientific Advanced Business Intelligence",
    author_email="alon@sabi.ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="Scientific, Advanced, Business, Intelligence",
    package_dir={"": "./"},
    packages=find_packages(),  # Required
    python_requires=">=3.6, <4",
    install_requires=["requests", "pycryptodome", "hashids", "jsonpickle", "pyjwt", "requests", "hashids", "rebel"],
    extras_require={"dev": ["boto3", "black"]},
)
