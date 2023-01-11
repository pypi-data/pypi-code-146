# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="ColorInfo3",
	version="1.1.0",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="ColorInfo3 是一个使用Python3编写的简单的彩色日志工具，拥有简单、友好的语法,完全通过Python内置模块实现，无需安装任何第三方依赖",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/ColorInfo3",
	packages=["ColorInfo3"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.0',
)
