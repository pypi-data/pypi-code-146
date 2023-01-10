from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
project_urls = {
  'HomePage': 'https://cwrusdle.bitbucket.io',
    'Documentation':'https://cwrusdle.bitbucket.io/fairmaterials-py/index.html'
}


setup(
    name='fairmaterials',
    version='0.2.0',
    keywords=['FAIRification','PowerPlant','Engineering'],
    description='Generate  JSON-LD format file based on FAIRification standard',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls=project_urls,
    author='Mingjian Lu,Liangyi Huang, Will Oltjen,Xuanji Yu,Arafath Nihar, Tommy Ciardi, Erika Barcelos,Pawan Tripathi,Abhishek Daundkar,Deepa Bhuvanagiri,Hope Omodolor,Hein Htet Aung,Kristen Hernandez,Mirra Rasmussen,Raymond Wieser, Sameera Nalin Venkat,Tian Wang, Weiqi Yue, Yangxin Fan,Rounak Chawla,Leean Jo,Zelin Li,Jiqi Liu, Justin Glynn, Kehley Coleman,Jeffery Yarus, Mengjie Li,Kristopher.Davis, Laura Bruckman,Yinghui Wu,Roger French',
    author_email='mxl1171@case.edu,lxh442@case.edu, wco3@case.edu,xxy530@case.edu ,arafath@case.edu,tgc17@case.edu,eib14@case.edu,pkt19@case.edu,aad157@case.edu,dcb117@case.edu,hxo76@case.edu,hxh483@case.edu,kjh125@case.edu,mmr125@case.edu,rxw497@case.edu,sxn440@case.edu,txw387@case.edu,wxy215@case.edu,yxf451@case.edu,rxc542@case.edu,yxj414@case.edu,zxl1080@case.edu,jxl1763@case.edu,jpg90@case.edu,kac196@case.edu,jmy41@case.edu,Mengjie.Li@ucf.edu,Kristopher.Davis@ucf.edu,lsh41@case.edu,yxw1650@case.edu,rxf131@case.edu',


    # BSD 3-Clause License:
    # - http://choosealicense.com/licenses/bsd-3-clause
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD License (BSD-3)',
    packages=find_packages(),
    include_package_data=True,
)