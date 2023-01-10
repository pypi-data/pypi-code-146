from setuptools import setup

setup(name='raster_basics',
      version='1.1.4',
      description='Basic GeoTIFF Processing',
      packages=['raster_basics'],
      author_email='awwells@andrew.cmu.edu',
      url='https://github.com/albinwwells/Raster-Basics',
      zip_safe=False)

# python setup.py sdist
# twine upload dist/*

# sudo pip install raster_basics --upgrade