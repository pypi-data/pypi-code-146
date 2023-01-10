from setuptools import setup, find_packages
import sys
with open('README.rst', 'r') as f:
    long_description = f.read()
setup(
	name = 'Xiaoimage',
	version = '2.1.9',
	packages = find_packages(),
        author = 'Wells Xiao',
        long_description=long_description,
	include_package_data = True,
        scripts=['./python-exe可执行程序/load-image.py', './python-exe可执行程序/baidu-image.py'],
	install_requires=[
		'Flask',
                'requests',
                'BeautifulSoup4',
	],
        entry_points="""
            [consle_scripts]
            xiaoimage = Xiaoimage:main
        """,
)
