from setuptools import setup, find_packages

setup(
	name = 'Xiaoimage',
	version = '1.0.0',
	packages = find_packages(),
	include_package_data = True,
	install_requires=[
		'Flask',
                'requests',
	],
        entry_points="""
[consle_scripts]
Xiaoimage = Xiaoimage:main
        """,
)
