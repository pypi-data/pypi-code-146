from setuptools import setup
import comfun

setup(
    name='comfun',
    version=comfun.__version__,
    packages=[
        'comfun',
    ],
    url='',
    license='',
    author='Roland Pfeiffer',
    author_email='',
    description='COMmonly used FUNctions',
    install_requires=[
        "opencv-python",
        "PyPDF2",
        "wget",
        "setuptools",
    ]
)
