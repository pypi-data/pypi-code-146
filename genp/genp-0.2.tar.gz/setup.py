import setuptools
with open(r'C:\Users\Iwan\Desktop\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='genp',
	version='0.2',
	author='VANECK',
	author_email='vingving648@gmail.com',
	description='This is simple python password generation lib.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/IvanIsak2000/password_generation_lib',
	packages=['genp'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)