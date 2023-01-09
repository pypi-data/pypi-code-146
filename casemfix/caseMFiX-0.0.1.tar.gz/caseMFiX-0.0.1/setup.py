import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import setup, find_packages

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()
setup(
    name='caseMFiX',
    version='0.0.1',
    license='GPLv3',
    description='Create and manipulate MFiX-DEM cases',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Ungjin Na',
    author_email='jinny942@postech.ac.kr',
    url='https://github.com/thesystempostech/thesystempostech_CFD',
    packages=find_packages('src'),
    package_dir={'': 'caseMFiX'},
    py_modules=[splitext(basename(path))[0] for path in glob('caseMFiX/src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering'
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/thesystempostech/thesystempostech_CFD'
    },
    keywords=[
        'cfd', 'MFiX-DEM', 'postProcessing'
    ],
    python_requires='>=3.6',
)
