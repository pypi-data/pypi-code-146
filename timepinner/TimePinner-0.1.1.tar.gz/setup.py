# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="TimePinner",
    version="0.1.1",
    author="g1879",
    author_email="g1879@qq.com",
    description="一个用于代码中计时的小工具。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="stopwatch",
    url="https://gitee.com/g1879/TimePinner",
    include_package_data=True,
    packages=find_packages(),
    install_requires=["TimePinner-stubs"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6'
)
