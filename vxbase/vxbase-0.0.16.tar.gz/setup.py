from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = open('requirements.txt').readlines()


setup(
    name='vxbase',
    version='0.0.16',
    description='Base for all clases and scripts in VauxooTools',
    long_description=readme,
    author='Tulio Ruiz',
    author_email='tulio@vauxoo.com',
    url='https://git.vauxoo.com/devops/vxbase',
    download_url='https://git.vauxoo.com/devops/vxbase',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='vauxootools vxbase',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    py_modules=['vxbase'],
    scripts=[]
)
