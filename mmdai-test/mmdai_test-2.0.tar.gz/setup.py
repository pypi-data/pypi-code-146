from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mmdai_test",                                      # 包的分发名称，使用字母、数字、_、-
    version="2.0",                                          # 版本号, 版本号规范：https://www.python.org/dev/peps/pep-0440/
    author="mmdai",                                         # 作者名字
    author_email="mmdai@shu.edu.cn",                        # 作者邮箱
    description="PyPI Tutorial",                            # 包的简介描述
    long_description=long_description,                      # 包的详细介绍(一般通过加载README.md)
    long_description_content_type="text/markdown",          # 和上条命令配合使用，声明加载的是markdown文件
    # url="https://github.com/",                              # 你这个项目的主页地址，也可以直接链接到你这个项目的Github 地址上面去。
    packages=find_packages(),                               # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，
    classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ],
    install_requires=['pymysql>=0.10.0', 'openpyxl>=3.0.5'],  # 依赖的包
    python_requires='>=3'
)

# 这是最简单的配置
# 有关详细信息，请参阅(https://packaging.python.org/guides/distributing-packages-using-setuptools/)
