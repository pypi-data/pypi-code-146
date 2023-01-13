import setuptools

setuptools.setup(
    name='pq_dataset',
    version='1.1.3',
    license='MIT',
    author="Christian Frost",
    author_email='anon@anon.com',
    packages=['pq_dataset', 'pq_dataset.utils'],
    url='https://github.com/ctf76/pqdataset',
    keywords='Project for working with dataset exports',
    install_requires=[
          'datetime',
          'numpy',
          'pandas',
          'pathlib',
          'lxml'
      ],
)