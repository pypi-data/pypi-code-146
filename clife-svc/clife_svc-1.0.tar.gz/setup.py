import setuptools

# Readme
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Module dependencies
requirements, dependency_links = [], []
with open('clife_svc/requirements.txt') as f:
    for line in f.read().splitlines():
        if line.startswith('-e git+'):
            dependency_links.append(line.replace('-e ', ''))
        else:
            requirements.append(line)

setuptools.setup(
    name='clife_svc',   # 需要打包的名字,即本模块要发布的名字
    version='1.00',     # 版本
    author='andy.hu',  # 作者名
    author_email='hlp0@163.com',  # 作者邮件
    description='A module for service',   # 简要描述
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',       # 项目地址,一般是代码托管的网站
    packages=setuptools.find_packages(),
    include_package_data=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    dependency_links=dependency_links,
    python_requires='>=3.6',
)
