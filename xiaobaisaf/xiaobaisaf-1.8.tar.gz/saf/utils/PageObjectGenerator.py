#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/10/21 10:03
@File  : PageObjectGenerator.py
'''

'''
样例：
# filename=tag_pages.yaml
---
pages:
    - 
        name: login
        description: 登录页
        url: https://192.168.0.106:8001/login
        elements:
            - 
                xpath: //input[1]
                action: send_keys
                data: xiaobai
            - 
                xpath: //input[2]
                action: send_keys
                data: 123456
            -
                xpath: //button
                action: click
    - 
        name: search
        description: 搜索页
        url: https://192.168.0.106:8001/search
        elements:
            - 
                xpath: //input[1]
                action: send_keys
                data: 小米
            -
                xpath: //button
                action: click
'''
from saf.utils.yamlUtils import yaml_reader
import os

step = '\\' if os.name == 'nt' else '/'

class PageObjectGenerator(object):
    def __init__(self, url: str = None, file: str = None, path: str = None):
        '''
        file: 指定单个需要转化的脚本名称
        path：指定批量需要转化脚本所在的目录
        '''
        self.url = url
        self.file = file
        self.path = path

    def yaml2json(self):
        '''  '''
        self.files = []
        self.datas = []
        self.path = self.path
        if self.file and os.path.isfile(self.file) and os.path.splitext(self.file)[1] in ['.yml', '.yaml']:
            self.files.append(self.file)
            self.datas.append(yaml_reader(file=self.file))
        elif self.path and os.path.isdir(self.path):
            self.files = [i for i in os.listdir(self.path) if os.path.splitext(i)[1] in ['.yml', '.yaml']]
            for file in self.files:
                self.datas.append(yaml_reader(file=self.path + step + file))
        else:
            raise ('您输入的地址有误，请确认！')

    def json2py(self, data: dict = None, file_name: str = '', path: str = '.'):
        '''
        json转为python代码
        data：json数据
        file_name：输出的脚本文件名称
        path：输出脚本保存的路径
        '''
        if 'pages' not in data.keys():
            ''' 不合规的yaml数据文件 '''
            return None
        path = os.path.abspath(path)
        new_file_name = os.path.splitext(file_name)[0] + '.py'
        print(f'\r正在解析：{path + step + file_name}', end='')
        code = '''#! /usr/bin/env python\
            \rfrom selenium import webdriver\
            \rfrom selenium.webdriver.common.by import By\
            \rfrom selenium.webdriver.common.keys import Keys  # 键盘事件\
            \rfrom selenium.webdriver.common.action_chains import ActionChains  # 鼠标事件\
            \r'''
        for page in data['pages']:
            ''' 解析：name、description、url、elements '''
            code += f'''\
                    \rclass {page['name']}PageObject(object):\
                    \r\t""" {page['description']} """\
                    \r\tdef __init__(self, driver):\
                    \r\t\tself.driver = driver\
                    \r\t\tif self.driver.current_url != '{page['url']}':\
                    \r\t\t\tself.driver.get('{page['url']}')\
                    \r'''
            for i, element in enumerate(page['elements']):
                if element['action'] == 'click':
                    code += f'''\
                    \r\tdef element_{i}(self):\
                    \r\t\tself.driver.find_element(by=By.XPATH, value='{element["xpath"]}').click()\
                    \r'''
                elif element['action'] == 'send_keys':
                    code += f'''\
                    \r\tdef element_{i}(self):\
                    \r\t\tself.driver.find_element(by=By.XPATH, value='{element["xpath"]}').send_keys('{element['data']}')\
                    \r'''
        print('\r正在转化...', end='')
        with open(file=path + step + new_file_name, mode='w', encoding='UTF-8') as f:
            f.write(code)
            f.close()
        print(f'\r脚本文件：{new_file_name} 已经生成成功，请查看.')

    def yaml2py(self):
        '''
        执行生成PageObject代码
        '''
        for i, file in enumerate(self.files):
            self.json2py(data=self.datas[i], file_name=self.files[i], path=self.path if self.path else '.')

    def url2html(self):
        '''
        解析URL所获取的HTML内容
        '''


def yaml2py(source: str = ''):
    if os.path.isdir(source):
        PageObjectGenerator(path=source).json2py()
    elif os.path.isfile(source):
        PageObjectGenerator(file=source).json2py()

def url2py():
    pass

# if __name__ == '__main__':
#     conver('../data')