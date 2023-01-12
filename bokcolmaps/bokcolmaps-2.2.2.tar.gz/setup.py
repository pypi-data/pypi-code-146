from setuptools import setup, find_packages

setup(name='bokcolmaps',
      version='2.2.2',
      description='Colourmap plots based on the Bokeh visualisation library',
      author='Systems Engineering & Assessment Ltd.',
      author_email='Marcus.Donnelly@sea.co.uk',
      url='https://bitbucket.org/sea_dev/bokcolmaps',
      license='MIT',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering'
                   ],
      keywords=['Bokeh',
                '2D Plot',
                '3D Plot'
                ],
      packages=find_packages(),
      install_requires=['numpy >= 1.20',
                        'bokeh >= 3'
                        ],
      include_package_data=True,
      )
