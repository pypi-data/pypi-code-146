import os
from setuptools import setup


def get_version(packname, filename='__init__.py', version_flag='version'):
    with open(os.path.join(packname, filename), 'r') as fp:
        while True:
            text = fp.readline()
            if not text:
                continue
            if text.startswith(version_flag):
                ver = eval(text.split('=')[1])
                return '.'.join(str(_) for _ in ver)
    raise RuntimeError('版本号查找错误')


setup(
    name='nsqdriver',
    version=get_version('nsqdriver'),
    author='Naishu Technology',
    author_email='jilianyi@naishu.tech',
    description='Naishu Q series quantum measurement and control equipment driver interface',
    url='https://g2hoyqcmh4.feishu.cn/wiki/wikcnzvyMd82DLZUe2NsI6HxsFc',
    packages=['nsqdriver', 'nsqdriver.wrapper'],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.18',
        'waveforms'
    ],

    classifiers=[
        # 开发的目标用户
        'Intended Audience :: Developers',

        # 目标 Python 版本
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)
