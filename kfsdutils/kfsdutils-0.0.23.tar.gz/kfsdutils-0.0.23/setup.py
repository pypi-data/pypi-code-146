from setuptools import setup, find_packages

setup(name='kfsdutils',
      version='0.0.23',
      description='Sample Pkg',
      long_description='Sample Pkg',
      long_description_content_type="text/markdown",
      author='nathangokul',
      author_email="nathangokul111@gmail.com",
      packages=['kfsdutils'],
      zip_safe=False,
      install_requires=[
            'netifaces',
            'PyYAML'
      ]
)
