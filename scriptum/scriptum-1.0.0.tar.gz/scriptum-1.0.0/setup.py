import setuptools

setuptools.setup(
    name="scriptum",
    version="1.0.0",
    author="Aarav Borthakur",
    author_email="gadhaguy13@gmail.com",
    description="A command line utility for storing, documenting, and executing your project's scripts",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gadhagod/scriptum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["jsonc-parser==1.1.5"],
    scripts=["./scr"],
    python_requires=">=3.6"
)