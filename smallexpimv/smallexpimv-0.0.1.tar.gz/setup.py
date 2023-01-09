from setuptools import find_packages

#######################################
# Prepare list of compiled extensions #
#######################################

extensions = []

# f2py extension 
# (to handle f2py extensions we need to replace the setup function and 
# the Extension class with their extended version from the numpy package)
from numpy.distutils.core import setup, Extension
extensions.append(
        Extension(
            name='smallexpimv.f_smallexpimv',
            sources=['src/smallexpimv/F_smallexpimv.F90'],
            libraries=['blas','lapack'])
        )

#########
# Setup #
#########

setup(
    version = "0.0.8",
    package_dir={"": "src"},
    ext_modules = extensions,
    packages=find_packages(where="src"),
    )

