import setuptools
from weepy import __version__

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="weepy",
	version=__version__,
	scripts=["tools/dev_server.py"],
	entry_points={
		'console_scripts': ['weepy=dev_server:server'],
	},
	author="Patrik Katrenak",
	author_email="patrik@katryapps.com",
	description="Tiny ASGI framework",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/katry/weepy",
	packages=["weepy"],
	install_requires=["orjson"],
	extras_require={
		"dev": ["python-daemon", "python-dotenv", "uvicorn[standard]", "requests", "pytest"]
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
		"Operating System :: OS Independent",
	],
	platforms=["any"],
	python_requires=">=3.9",
)
