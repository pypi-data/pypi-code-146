
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ensdat",
    version="0.0.1",
    author="Aqouthe",
    author_email="hoonie0929@gmail.com",
    description="encryption module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aqouthe",
    classifiers=[
        "Topic :: Security :: Cryptography",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'pycryptodome',
        'pycryptodomex'
    ]
)