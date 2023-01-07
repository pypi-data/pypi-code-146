from pathlib import Path
from setuptools import setup
from src import skrutable

this_directory = Path(__file__).parent
readme = (this_directory / "src/skrutable/README.md").read_text()

setup(
    name='skrutable',
    version=skrutable.__version__,
    description="skrutable library for working with Sanskrit text",
    long_description=readme,
    long_description_content_type='text/markdown',
    license='CC BY-SA 4.0',
    author="Tyler Neill",
    author_email='tyler.g.neill@gmail.com',
    package_dir={'': 'src'},
    packages=["skrutable"],
    py_modules=[
        "skrutable.transliteration",
        "skrutable.scansion",
    	"skrutable.meter_identification", 
    	"skrutable.splitter.wrapper",
    ],
    package_data={'': [
		'config.json', 
		'manual.md'
	]},
    url='https://github.com/tylergneill/skrutable',
    keywords='Sanskrit text transliteration scansion meter sandhi compound splitting',
    install_requires=[
        # 'requests',
        # 'numpy',
        # 'jupyter'
      ],

)