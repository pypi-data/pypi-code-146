try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools


setup(
    name='my_retry',
    author='yrq',
    version='0.1.0',
    license='MIT',

    description='Retry module, You can choose to raise error or return the specified parameters',
    author_email='1307272972@qq.com',
    url='https://github.com/Yternal/my_retry',
    # 包内需要引用的文件夹
    packages=["my_retry"],

    # 依赖包
    install_requires=[
        'loguru >= 0.6.0'
    ],
    zip_safe=True,
)
