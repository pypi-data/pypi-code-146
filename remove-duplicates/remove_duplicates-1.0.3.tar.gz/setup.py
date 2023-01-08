#!/usr/bin/env python
import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="remove_duplicates",
    version="1.0.3",
    author="Roman Shevchik",
    author_email="goctaprog@gmail.com",
    description="Utility to recursive search and move/delete duplicate files of the same size and "
                "context in specified folder.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octaprog7/remove_duplicates",
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    python_requires='>=3.7.2,<3.12',
    entry_points={
        'console_scripts': [
            'rmdup = remove_duplicates.remove_dup:main',
        ],
    }
)
