from setuptools import setup, find_packages

setup(name='kfsdutils',
      version='0.0.33',
      description='Sample Pkg',
      long_description='Sample Pkg',
      long_description_content_type="text/markdown",
      author='nathangokul',
      author_email="nathangokul111@gmail.com",
      packages=find_packages(),
      include_package_data = True,
      zip_safe=False,
      install_requires=[
            'netifaces',
            'PyYAML'
      ]
)
