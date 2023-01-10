from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.2'
DESCRIPTION = 'Easy way to connect hardware and use gpio in raspberry pico'
PACKAGE_NAME = 'gpiopico'
AUTHOR = 'Irvyn Cornejo'
EMAIL = 'irvyncornejo@gmail.com'
GITHUB_URL = 'https://github.com/irvyncornejo/hwlib/tree/main/raspberry-pico/rpi-gpio-pico'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = ['raspberry-pi pico', 'rpi-pico'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)