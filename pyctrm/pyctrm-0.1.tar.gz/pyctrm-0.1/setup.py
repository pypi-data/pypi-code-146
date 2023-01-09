import setuptools
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(
    name='pyctrm',
    version='0.01',
    description='大宗商品风控贸易管理通用策略方法',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Wang Qi',
    author_email='wangmarkqi@gmail.com',
    url='https://gitee.com/wangmarkqi/pyctrm',
    packages=setuptools.find_packages(),
    keywords=['大众商品贸易', '风险控制', '波动率',"VAR","risk"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',

)


'''
# 上传source 包
python setup.py sdist
twine upload dist/*

'''
