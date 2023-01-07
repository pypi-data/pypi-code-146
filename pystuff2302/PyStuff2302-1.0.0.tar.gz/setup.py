from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'Sample Package made for a demo \
	of its making for the GeeksforGeeks Article.'

setup(
		name ='PyStuff2302',
		version ='1.0.0',
		author ='Arnav Dadarya',
		author_email ='ardada2468@gmail.com',
		url ='https://github.com/ardada2468/pystuff',
		description ='Demo Package for testing.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'test = pystuff.test:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='arnav dadarya',
		install_requires = requirements,
		zip_safe = False
)
