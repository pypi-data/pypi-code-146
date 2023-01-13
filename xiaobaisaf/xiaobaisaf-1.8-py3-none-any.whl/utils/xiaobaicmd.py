#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/24 2:26
@File  : xiaobaicmd.py
'''
import os.path
from shutil import copytree
import click
from saf.utils.PageObjectGenerator import yaml2py

@click.command()
@click.option('--template', '-t', type=click.Choice(['web', 'api', 'app']), nargs=1, help='创建自动化项目模板')
@click.option('--dirname', '-d', default='.', type=str, nargs=1, help='创建自动化项目模板存放的目录')
@click.option('--yaml', '-y', default='.', type=str, nargs=1, help='需要转化PageObject对象代码的文件(夹)名')
def main(template, dirname, conversion):
    if template:
        if "web" == template.lower():
            copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\web'),
                     os.path.join(os.path.abspath(dirname), 'web')
                     )
        elif "api" == template.lower():
            copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\api'),
                     os.path.join(os.path.abspath(dirname), 'api')
                     )
        elif "app" == template.lower():
            copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\app'),
                     os.path.join(os.path.abspath(dirname), 'app')
                     )
        else:
            raise ("您输入的数据有误，有效范围：web 或 api 或 app")
    elif conversion:
        yaml2py(source=conversion)

# if __name__ == '__main__':
#     main()