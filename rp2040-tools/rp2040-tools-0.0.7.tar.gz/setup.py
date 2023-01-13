from setuptools import setup, find_packages

setup(
    name='rp2040-tools',  # 包名
    version='v0.0.7',  # 版本
    description="Some tools for RP2040",  # 包简介
    long_description=open('README.md', encoding='utf-8').read(),  # 读取文件中介绍包的详细内容
    long_description_content_type='text/markdown',
    include_package_data=True,  # 是否允许上传资源文件
    author='曾钦李',  # 作者
    author_email='1838696034@qq.com',  # 作者邮件
    maintainer='',  # 维护者
    maintainer_email='',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='',  # 设置python版本要求
    install_requires=[],  # 安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },  # 设置命令行工具(可不使用就可以注释掉)
)
