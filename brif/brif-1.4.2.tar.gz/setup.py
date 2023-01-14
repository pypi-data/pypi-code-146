from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import platform

if platform.system() == 'Windows':
    extra_flags = ['/openmp']
    extra_link = []
elif platform.system() != 'Darwin':
    extra_flags = ['-fopenmp']
    extra_link = ['-lgomp']
else:
    extra_flags = []
    extra_link = []

setup(name='brif',
      version="1.4.2",
      description = "Build decision trees and random forests for classification and regression.",
      author = 'Yanchao Liu',
      author_email = 'yanchaoliu@wayne.edu',
      url = 'https://pypi.org/project/brif/',
      packages = ['brif'],
      ext_modules=[
          Extension('brifc',
                    ['pybrif.c','brif.c'],
                    extra_compile_args = extra_flags,
                    extra_link_args = extra_link
                    )
          ]
      )
