from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.11'
DESCRIPTION = "Record Window (hwnd) and save the recording as mp4 (normalized fps) - Works even with background windows"

# Setting up
setup(
    name="window2video",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/window2video',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_cv_imwrite_imread_plus', 'ctypes_screenshots', 'get_video_len', 'keyboard', 'list_files_with_timestats', 'make_even_odd', 'pandas', 'plyer'],
    keywords=['file path', 'windows'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_cv_imwrite_imread_plus', 'ctypes_screenshots', 'get_video_len', 'keyboard', 'list_files_with_timestats', 'make_even_odd', 'pandas', 'plyer'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*