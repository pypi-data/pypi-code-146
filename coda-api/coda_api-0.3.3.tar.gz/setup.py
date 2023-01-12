from setuptools import setup

setup(name='coda_api',
      version='0.3.3',
      description='CODA platform API',
      url='https://github.com/coda-platform/python-api',
      author='Louis Mullie',
      license='GPL',
      py_modules=["coda_api"],
      packages=['coda_api'],
      install_requires=['numpy', 'requests'],
      zip_safe=False)