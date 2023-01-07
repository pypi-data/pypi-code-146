import setuptools
f = open('README.md','r',encoding='utf-8')
setuptools.setup(
    name="ycolor", # Replace with your own username #自定义封装模块名与文件夹名相同
    version="1.0.5", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="Yourourchour", #作者
    author_email="348422509@qq.com", #邮箱
    description="A convenient color text printing tool", #描述
    long_description = f.read(),
    packages=setuptools.find_packages(),
)
f.close()
