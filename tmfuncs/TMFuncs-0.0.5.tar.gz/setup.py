import shutil
import subprocess

from setuptools import setup, find_packages

# 读取模块详细说明
with open("README.md", "r") as fh:
    long_description = fh.read()


# 获取该包的最新版本
def get_latest_version(package_name):
    output = subprocess.run(["pip", "index", "versions", package_name],
                            capture_output=True)
    output = output.stdout.decode('utf-8')
    if output:
        output = list(filter(lambda x: len(x) > 0, output.split('\n')))
        latest_version = output[-1].split(':')[1].strip()
        return latest_version
    else:
        return None


# 拆分版本号
def split_version(v):
    return v.split('.')


PACKAGE_NAME = 'TMFuncs'
# 获取该包的最新版本
try:
    current_version = get_latest_version(PACKAGE_NAME)
    v1, v2, v3 = split_version(current_version)
except Exception as _:
    v1, v2, v3 = 0, 0, 0

# 清空dist的原有包
shutil.rmtree('dist')

# 构建新的包并生成到dist目录
setup(name=PACKAGE_NAME,
      version=f'{int(v1)}.{int(v2)}.{int(v3) + 1}',  # 默认就是v3基础上 +1
      description='Databricks common functions, written by TrueMetrics.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://www.truemetrics.cn/',
      author='TSO',
      author_email='tlsong@truemetrics.cn',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
