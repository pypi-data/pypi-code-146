from setuptools import setup, find_packages

setup(
	name = 'Xiaoimage',
	version = '2.0.1',
	packages = find_packages(),
	include_package_data = True,
	install_requires=[
		'Flask',
                'requests',
	],
        entry_points="""
            [consle_scripts]
            Ximg = Ximg:main
        """,
)
