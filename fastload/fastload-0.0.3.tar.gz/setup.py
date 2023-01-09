from pathlib import Path
from setuptools import setup, find_packages

VERSION = '0.0.3' 

this_directory = Path(__file__).parent
DESCRIPTION = 'A Fast File Downloader For Python'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
        name="fastload", 
        version=VERSION,
        author="Danish Anodher",
        author_email="",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'downloader', 'file_downloader', 'fast_downloader', 'download'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)