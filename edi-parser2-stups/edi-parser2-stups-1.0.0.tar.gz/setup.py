import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    'pandas'
]

tests_require = [
    'pytest'
]

setuptools.setup(
    name="edi-parser2-stups",
    version="1.0.0",
    author="Justin Stuparitz",
    author_email="justinstuparitz@gmail.com",
    description="A library of EDI file format parsers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires='>=3.9.0',
)