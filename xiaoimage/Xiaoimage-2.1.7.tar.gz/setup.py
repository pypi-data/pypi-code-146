from setuptools import setup, find_packages
import sys
sys.argv = ['python','sdist', 'bdist_wheel']
setup(
	name = 'Xiaoimage',
	version = '2.1.7',
	packages = find_packages(),
        author = 'Wells Xiao',
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
