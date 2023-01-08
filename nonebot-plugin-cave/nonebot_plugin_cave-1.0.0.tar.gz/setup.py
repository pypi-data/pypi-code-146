from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r",encoding='utf-8') as f:
  long_description = f.read()

setup(
    name='nonebot_plugin_cave',
    version='1.0.0',
    description='A small example package',
    long_description=long_description,
    author='hmzz804',
    author_email='2166908863@qq.com',
    url='https://github.com/hmzz804',
    install_requires=[],
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 开发的目标用户
        'Intended Audience :: Developers',
        # 属于什么类型
        'Topic :: Software Development :: Build Tools',
        # 许可证信息
        'License :: OSI Approved :: MIT License',
        # 目标 Python 版本
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
'''
name：项目的名称，name是包的分发名称。
version：项目的版本。需要注意的是，PyPI上只允许一个版本存在，如果后续代码有了任何更改，再次上传需要增加版本号
author和author_email：项目作者的名字和邮件, 用于识别包的作者。
description：项目的简短描述
long_description：项目的详细描述，会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
packages：指定最终发布的包中要包含的packages。
install_requires：项目依赖哪些库，这些库会在pip install的时候自动安装
classifiers：其他信息，一般包括项目支持的Python版本，License，支持的操作系统。

作者：测试开发技术
链接：https://www.jianshu.com/p/890a1ab79b76
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

'''