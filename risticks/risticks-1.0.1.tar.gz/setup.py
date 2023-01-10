import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

requirements = ["requests>=2.21.0"]

setuptools.setup(
	name="risticks",
	version="1.0.1",
	author="pip64, ierhon",
	author_email="mrpip64@mail.ru",
	description="Библиотека для удобной работы с API Risticks",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/pip64/risticks-api",
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
)