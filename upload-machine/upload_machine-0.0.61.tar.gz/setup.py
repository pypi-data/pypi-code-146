from setuptools import setup, find_packages
import io

setup(
    name = "upload_machine",     
    version = "0.0.61", 
    keywords = ["pip", "autoupload","auto","upload","PT","private tracker"],            
    description = "Upload local resources to PT trackers automatically.",    
    long_description=io.open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license = "MIT Licence",    

    entry_points = {
        'console_scripts': [
            'upload_machine=upload_machine.main:main',
            'um=upload_machine.main:main',
        ],
    },

    url = "https://github.com/dongshuyan/Upload_Machine", 
    author = "sauterne",            
    author_email = "ssauterne@qq.com",

    packages = find_packages(),
    include_package_data = True,
    exclude_package_data = {'': ['__pycache__']},

    platforms = "any",
    python_requires = '>=3.9.0',
    install_requires = ["loguru","pathlib","typing","lxml","pyyaml","requests","bs4","datetime","qbittorrent-api","function_controler","doubaninfo >= 0.0.13","cloudscraper","progress","torf"]
)