# 编写完包源码后，python setup.py sdist生成pip压缩包
# 解压压缩包，python setup.py install  安装自己的包，就可以引用了


from distutils.core import setup, Extension
from setuptools import find_packages

setup(name='squishtest',  # 包名
      version='2023.1',  # 版本号
      description='',
      long_description='',
      author='lpq',
      author_email='825485697@qq.com',
      url='https://blog.csdn.net/luanpeng825485697',
      license='',
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.10',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=['squishtest'],
      package_dir={'squishtest': 'src/squishtest'},
      package_data={'squishtest': ['lib/*.dll', 'lib/*.pyd']},
      include_package_data=True,
      )

