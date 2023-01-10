from setuptools import setup, find_packages

setup(
	name = 'Xiaoimage',
	version = '1.1.3',
	packages = find_packages(),
	include_package_data = True,
        scripts=['./python-exe可执行程序/load-image.py'],
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
