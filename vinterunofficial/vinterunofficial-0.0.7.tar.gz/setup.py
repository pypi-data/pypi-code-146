from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(
	name="vinterunofficial",
	version="0.0.7",
	description="This is a unofficial wrapper for Vinter.co API",
	long_description=long_description,
	long_description_content_type='text/markdown',
	install_requires=["requests==2.28.1"],
	author="Rahul Mistri",
	author_email="rahulmistri1997@gmail.com",
	packages=find_packages(),
)