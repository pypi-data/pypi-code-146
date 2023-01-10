from setuptools import setup, find_packages

setup(
	name = 'Xiaoimage',
	version = '2.1.5',
	packages = find_packages(),
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
