from setuptools import setup, find_packages

extras = {}

setup(name='python-ilorest-library',
      version='4.0.0.1',
      description='iLO Rest Python Library',
	  author = 'Hewlett Packard Enterprise',
	  author_email = 'rajeevalochana.kallur@hpe.com',
      extras_require = extras,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Communications'
      ],
      keywords='Hewlett Packard Enterprise',
      url='https://github.com/HewlettPackard/python-ilorest-library',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          'jsonpatch',
          'jsonpath_rw',
          'jsonpointer',
          'urllib3',
          'six'
      ])
