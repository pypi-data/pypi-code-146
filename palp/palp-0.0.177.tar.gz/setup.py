from setuptools import setup, find_packages  # 这个包没有的可以pip一下

file_path = './palp/README.md'

setup(
    name="palp",  # 这里是pip项目发布的名称
    version="0.0.177",  # 版本号，数值大的会优先被pip
    keywords=["palp", "scrapy", "feapder"],  # 关键字
    description="一个 爬虫框架",  # 描述
    long_description=open(file_path, 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",  # 许可证

    url="https://github.com/Leviathangk/palp",  # 项目相关文件地址，一般是github项目地址即可
    author="郭一会儿",  # 作者
    author_email="1015295213@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'zmail', 'requests', 'quickdb', 'pybloom-live', 'parsel', 'loguru', 'chardet', 'beautifulsoup4', 'gsender',
        'dill'
    ],

    # 使得可以命令行访问
    entry_points={
        'console_scripts': [
            'palp = palp.tool.shell:main'
        ]
    }
)
