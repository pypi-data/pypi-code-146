import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="POTHEAD",
    version="0.7.3",
    author="Ulrik Mikaelsson",
    author_email="ulrik.mikaelsson@gmail.com",
    description="A reverse-http proxy implementation for non-concurrent requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rawler/pothead",
    packages=setuptools.find_packages(),
    install_requires=["psutil", "werkzeug"],
    tests_require=["aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
