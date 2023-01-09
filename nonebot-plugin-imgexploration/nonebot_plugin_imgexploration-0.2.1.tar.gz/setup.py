
import setuptools
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r",encoding="utf-8") as fd:
    long_description = fd.read()


setuptools.setup(

    name="nonebot_plugin_imgexploration",

    version="0.2.1",

    description="Google、Yandx和基于PicImageSearch的saucenao、ascii2d搜图",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/cpuopt/nonebot_plugin_imgexploration",

    author="cpufan",

    author_email="554950835@qq.com",

    packages=["nonebot_plugin_imgexploration"],

    install_requires=[
        "httpx>=0.23.1",
        "loguru>=0.6.0",
        "lxml>=4.9.2",
        "nonebot2>=2.0.0rc2",
        "Pillow>=9.3.0",
        "nonebot2>=2.0.0rc2", 
        "nonebot-adapter-onebot>=2.2.0",
        "nonebot-plugin-guild-patch>=0.2.1",
        "PicImageSearch>=3.7.4",
    ],
   
    classifiers=(
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
    ),
   
    keywords="ssh linux",
  
)
