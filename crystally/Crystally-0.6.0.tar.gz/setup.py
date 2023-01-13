import setuptools


def readme():
    with open('README.md') as f:
        return f.read()

project_urls = {
         "Documentation": "https://crystally.readthedocs.io/",
     }

setuptools.setup(name='Crystally',
                 version='0.6.0',
                 description='Python module to model and analyze crystal structures',
                 url='https://git.rwth-aachen.de/john.arnold/Crystally.git',
                 author='John Arnold',
                 author_email='john.arnold@rwth-aachen.de',
                 license='None',
                 packages=setuptools.find_packages(),
                 package_dir={'crystally': 'crystally'},
                 install_requires=['numpy', 'scipy>=1.7.0'],
                 python_requires='>=3.7',
                 project_urls=project_urls,
                 license_files=('LICENSE.md',),
                 long_description=readme(),
                 long_description_content_type="text/markdown")
