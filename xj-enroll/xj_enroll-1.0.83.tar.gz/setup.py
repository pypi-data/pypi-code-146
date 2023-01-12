# encoding: utf-8
"""
@project: djangoModel->setup
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 模块打包文件
@created_time: 2022/6/18 15:14
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as fp:
    log_desc = fp.read()

setup(
    name='xj_enroll',  # 模块名称
    version='1.0.83',  # 模块版本
    description='报名模块',  # 项目 摘要描述
    long_description=log_desc,  # 项目描述
    long_description_content_type="text/markdown",  # md文件，markdown格式
    author='赵向明',  # 作者
    author_email='sieyoo@163.com',  # 作者邮箱
    maintainer="孙楷炎",  # 维护者
    maintainer_email="sky4834@163.com",  # 维护者的邮箱地址
    packages=find_packages(),  # 系统自动从当前目录开始找包
    license="apache 3.0",
    install_requires=[]
)
