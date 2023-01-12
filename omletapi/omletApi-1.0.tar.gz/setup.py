from setuptools import setup

setup(name='omletApi',
      version='1.0',
      description='using omAPI',
      packages=['omletApi'],
      author_email='thekip077@gmail.com',
      zip_safe=False,
      install_package=["requests", "lxml", "bs4"]
)