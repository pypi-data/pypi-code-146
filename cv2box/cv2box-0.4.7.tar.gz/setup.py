#!/usr/bin/env python
# coding: utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cv2box',  # 项目的名称
    version='0.4.7',  # 项目版本
    author='ykk648',  # 项目作者
    author_email='ykk648@gmail.com',  # 作者email
    url='https://github.com/ykk648/cv2box',  # 项目代码仓库
    project_urls={
        "Bug Tracker": "https://github.com/ykk648/cv2box/issues",
    },
    description='cv toolbox',  # 项目描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    # package_dir={"": "src"},
    packages=setuptools.find_packages(),
    extras_require={"light": [],
                    "full": ['apscheduler', 'numexpr', 'h5py', 'yaml']},
    install_requires=['numpy', 'tqdm', 'opencv_python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
