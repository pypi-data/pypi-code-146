from setuptools import find_packages, setup

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="tololib",
    description="Python Library for Controlling TOLO Sauna/Steam Bath Devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Matthias Lohr",
    author_email="mail@mlohr.com",
    url="https://gitlab.com/MatthiasLohr/tololib",
    license="MIT",
    install_requires=[],
    python_requires=">=3.7, <4",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"tololib": ["py.typed"]},
    entry_points={"console_scripts": ["tolo-cli=tololib.cli:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Home Automation",
        "Typing :: Typed",
    ],
    project_urls={
        "Documentation": "https://matthiaslohr.gitlab.io/tololib/",
        "Source": "https://gitlab.com/MatthiasLohr/tololib",
        "Tracker": "https://gitlab.com/MatthiasLohr/tololib/issues",
    },
)
