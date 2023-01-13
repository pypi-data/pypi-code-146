from setuptools import setup, find_packages

setup(name='slack_hero',
      version='0.1',
      description='A package that enables you to easily exception messages from django to slack',
      packages=find_packages(),
      python_requires=">=3.6",
      install_requires=('slack_sdk>=3.13.0',),
      )
