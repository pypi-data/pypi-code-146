from setuptools import setup, find_packages

setup(
    name="mycustmpkg",
    version="0.0.1",
    license="MIT",
    author="Lucifer",
    author_email="lucifer@lucifer.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://www.google.com/",
    keywords="dummy custom package",
    install_requires=[
        "python-environ"
    ]
)