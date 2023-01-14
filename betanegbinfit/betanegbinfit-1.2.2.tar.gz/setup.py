from setuptools import setup, find_packages
from betanegbinfit import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(	
      install_requires=['scipy', 'numpy', 'pandas', 'jax', 'jaxlib', 'gmpy2', 'mpmath'],
      include_package_data=True,
      name="betanegbinfit",
      version=__version__,
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      python_requires=">=3.7",
      classifiers=[
              "Programming Language :: Python :: 3.7",
	      "Programming Language :: Python :: 3.8",
	      "Programming Language :: Python :: 3.9",
	      "Programming Language :: Python :: 3.10",
	      "Programming Language :: Python :: 3.11",
	      "Development Status :: 5 - Production/Stable",
	      "Topic :: Scientific/Engineering",
              "Operating System :: OS Independent"])
