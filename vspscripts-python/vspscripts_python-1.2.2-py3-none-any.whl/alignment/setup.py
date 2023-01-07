import os
import glob

from setuptools import setup, Extension
# from distutils.core import setup, Extension

requirements = ["opencv"]

def get_extensions():
    extensions_dir = os.path.dirname(__file__)
 
    main_file = glob.glob(os.path.join(extensions_dir, "*.cpp"))
    source = glob.glob(os.path.join(extensions_dir, "Clibrary", "src", "*.cpp"))
 
    sources = main_file + source

    # sources = [os.path.join(extensions_dir, s) for s in sources]

    include_dirs = [
        "/usr/include",
        "/usr/local/include/opencv4",
        os.path.join(extensions_dir, "Clibrary", "include")
    ]
 
    ext_modules = [
        Extension(
            "cModPyAlignment",
            sources=sources,
            include_dirs=include_dirs,
            libraries=['opencv_core', 'opencv_highgui', 'opencv_imgproc', 'opencv_imgcodecs', 'python3.6m'],
            # library_dirs=['/usr/local/lib64'],
            # extra_objects=[]
        )
    ]
 
    return ext_modules

# module = Extension('cModPyAlignment', sources=['cModPyAlignment.cpp'])

if __name__ == '__main__':

    setup(
        name='cModPyAlignment',
        version='1.0',
        description='This is the setup of cModPyAlignment',
        author='WJG',
        author_email='wangjiangong2018@ia.ac.cn',
        url='http://git.optima-hk.work:3000/jack/vspscripts/src/master/vspscripts/aligmentation',
        ext_modules = get_extensions()
    )
