from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
  name = 'CuttApi',         
  packages = ['CuttApi'],   
  version = '0.2.1.1',      
  license='MIT',        
  description = 'One of the best ways of shortening URLs using Cuttly URL shortener just by entering your API key and seeing the rest that is done automatically by the Module',   
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Devraj Therani',                   
  author_email = 'ttctlc96e@mozmail.com',      
  url = 'https://github.com/devrajtherani/CuttApi',   
  download_url = 'https://github.com/devrajtherani/CuttApi/archive/refs/tags/v_0.2.1.1.tar.gz',    
  keywords = ['API', 'SIMPLE'],   
  install_requires=[            
          'requests',
          'urllib3',
          'pyperclip'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)