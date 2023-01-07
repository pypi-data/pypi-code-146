from setuptools import setup, find_packages
import io

setup(
    name = "doubaninfo",     
    version = "0.0.13", 
    keywords = ["pip", "doubaninfo","douban","movie","book","PTGen","private tracker","PT"],            
    description = "Get douabn information to a summary text.",    
    long_description=io.open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license = "MIT Licence",    

    entry_points = {
        'console_scripts': [
            'doubaninfo=doubaninfo.main:main',
            'di=doubaninfo.main:main',
        ],
    },

    url = "https://github.com/dongshuyan/doubaninfo", 
    author = "sauterne",            
    author_email = "ssauterne@qq.com",

    packages = find_packages(),
    include_package_data = True,
    exclude_package_data = {'': ['__pycache__']},

    platforms = "any",
    python_requires = '>=3.7.0',
    install_requires = ["requests","bs4","argparse","pyperclip"]
)