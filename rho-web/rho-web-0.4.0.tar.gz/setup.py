import re
import ast
import os
import shutil

from setuptools import setup, find_packages


do_cythonize = os.getenv('CYTHONIZE', 'false').lower() == 'true'
ext_modules = []
cmdclass = {}
packages = find_packages(exclude=["tests"])

if do_cythonize:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext

        class MyBuildExt(build_ext):
            def run(self):
                build_ext.run(self)
                build_dir = os.path.realpath(self.build_lib)
                root_dir = os.path.dirname(os.path.realpath(__file__))
                target_dir = build_dir if not self.inplace else root_dir
                self.copy_file('rho_web/__init__.py', root_dir, target_dir)

            def copy_file(self, path, source_dir, destination_dir):
                if os.path.exists(os.path.join(source_dir, path)):
                    shutil.copyfile(os.path.join(source_dir, path),
                                    os.path.join(destination_dir, path))

        cmdclass['build_ext'] = MyBuildExt
        ext_modules = cythonize("rho_web/*.py")
        packages = []

    except ImportError:
        pass


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('rho_web/__init__.py', 'rb') as f:
    __version__ = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='rho-web',
    version=__version__,
    description="Contains common utilities for web development",
    long_description=open('README.md', 'r').read(),
    maintainer="Rho AI Corporation",
    license="Commercial",
    url="https://bitbucket.org/rhoai/rho-web",
    packages=packages,
    include_package_data=True,
    install_requires=[
        'Flask'
    ],
    ext_modules=ext_modules,
    extras_require={
        'dev': [
            'cython'
        ],
        'smorest': [
            'flask-smorest'
        ]
    },
    cmdclass=cmdclass
)
