from setuptools import setup, find_packages

setup(name='eskriper',
      version='0.2.2',
      description='Python helper utilities',
      author='Kristian Marlowe Ole',
      author_email='krismar.ole@gmail.com',
      license='GPLv3+',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.8'
)
