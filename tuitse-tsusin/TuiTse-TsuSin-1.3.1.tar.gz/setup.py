from distutils.core import setup

from panpun import PANPUN


setup(
    name='TuiTse-TsuSin',
    description='對齊資訊',
    long_description='共兩句漢羅對--起-來，掠出字數落勾ê位a̍h-sī無合教典ê用字',
    packages=['tuitse'],
    version=PANPUN,
    author='Tshuà Bûn-lī',
    author_email='ithuan@ithuan.tw',
    url='https://ithuan.tw/',
    download_url='https://github.com/i3thuan5/TuiTse-TsuSin',
    keywords=[
        'Parser', 'Alignment', 'Taigi', 'Hanji', 'Lomaji', 
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'kau3-tian2-iong7-ji7>=2.1.0',
    ],
)
