from setuptools import setup, find_packages

def requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="hashcore",
    version="0.1.1",
    author="Mouhsen Ibrahim",
    author_email="mouhsen.ibrahim@gmail.com",
    description="A tool for managing resources in a mono repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src", "tests": "tests"},
    python_requires='>=3.7',
    entry_points={"console_scripts": ["hashc=hash.cli:main"]},
    packages=find_packages('src'),
    install_requires=requirements(),
)
