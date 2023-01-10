import sys
from os import path
from setuptools import setup, find_packages
import yhgit

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yhgit',  # How you named your package folder (MyLib)
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'yhgit = yhgit.yhgit:main'
          ]
    },
    python_requires='>=3.7',
    version='2.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='yh branch git manager util',  # Give a short description about your library
    author='yonghuifan21',  # Type in your name
    author_email='jackfan1@yonghui.com',  # Type in your E-Mail
    url='http://gitlab.yonghui.cn/operation-xm-qdjg/yhgit.git',  # Provide either the link to your github or to your website
    download_url='https://files.pythonhosted.org/packages/08/7d/95aa3aa88c4c195889993de691b7fe816ac8d0767ea22fce56ccd240169a/yhmgit-0.3.tar.gz',  # I explain this later on
    keywords=['yhgit', 'git', 'yh'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'ruamel.yaml',
        'datetime',
        'GitPython',
        'runcmd',
        'prettytable',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

)
