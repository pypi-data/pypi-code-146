from setuptools import setup, find_packages

REQUIRED = ["pyquery", "qasync", "jinja2"]
setup(
    name = "mvvmQt" ,
    version = "0.33.9" ,
    description = "write qt like html" ,
    author = "Norman",
    author_email = "332535694@qq.com",
    url = "https://gitee.com/zhiyang/py-qt-dom",
    packages = find_packages(),
    python_requires = '>=3.6.0',
    install_requires = REQUIRED
)