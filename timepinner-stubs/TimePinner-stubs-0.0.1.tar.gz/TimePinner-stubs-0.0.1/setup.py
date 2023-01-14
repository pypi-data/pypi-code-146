# -*- coding:utf-8 -*-
from setuptools import setup  # , find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="TimePinner-stubs",
    version="0.0.1",
    author="g1879",
    author_email="g1879@qq.com",
    description="TimePinner的存根",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="stopwatch",
    url="https://gitee.com/g1879/TimePinner",
    include_package_data=True,
    package_data={"TimePinner-stubs": ["*.pyi", "*/*.pyi"]},
    packages=["TimePinner-stubs"],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6'
)
