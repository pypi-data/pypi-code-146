from setuptools import setup, find_packages

def requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

setup(
    name="hashcore",
    version="0.1.0",
    package_dir={"": "src", "tests": "tests"},
    entry_points={"console_scripts": ["hashc=hash.cli:main"]},
    packages=find_packages('src'),
    install_requires=requirements(),
)
