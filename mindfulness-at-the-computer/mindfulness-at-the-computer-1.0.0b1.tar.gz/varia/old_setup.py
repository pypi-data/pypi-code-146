# -there's no setuptools.command.uninstall (or similar)
import os.path

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import matc.constants

"""
PLEASE NOTE: If a wheel (bdist) is installed then pip doesn't run setup.py

> pip doesn't run setup.py from a wheel hence you cannot run any post-installation code from 
setup.py in a wheel.
--- https://stackoverflow.com/a/56495693/2525237

See also: https://stackoverflow.com/a/24749871/2525237

If using only sdist and if the building of the wheel fails during installation (after having 
downloaded the sdist)
there is a deprecation warning:
```
DEPRECATION: mindfulness-at-the-computer was installed using the legacy 'setup.py install' 
method, because a wheel
could not be built for it. A possible replacement is to fix the wheel build issue reported above. 
Discussion can be
found at https://github.com/pypa/pip/issues/8368
```

bdists vary depending on the platform

More info about sdist and bdist: https://dev.to/icncsx/python-packaging-sdist-vs-bdist-5ekb

"""

setup_file_dir: str = os.path.dirname(os.path.abspath(__file__))
appl_res_dir: str = os.path.join(setup_file_dir, "matc", "res")


def import_and_do_extra_setup():
    import matc.shared  # -only imported after install.run(self) / develop.run(self)
    matc.shared.do_extra_setup()


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        import_and_do_extra_setup()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        import_and_do_extra_setup()


"""
To completely uninstall/remove the application on Ubuntu, its dependencies, and .desktop files:

pip3 uninstall mindfulness-at-the-computer

$ pip3 uninstall mindfulness-at-the-computer 
Found existing installation: mindfulness-at-the-computer 1.0.0a10
Uninstalling mindfulness-at-the-computer-1.0.0a10:
  Would remove:
    /home/sunyata/.local/bin/mindfulness-at-the-computer
    /home/sunyata/.local/lib/python3.10/site-packages/matc/*
    /home/sunyata/.local/lib/python3.10/site-packages/mindfulness_at_the_computer-1.0.0a10.dist
    -info/*
Proceed (Y/n)? 

pip3 uninstall PySide6
pip3 uninstall shiboken6
rm ~/.local/share/applications/mindfulness-at-the-computer.desktop
rm ~/.config/autostart/mindfulness-at-the-computer.desktop
rm ~/Desktop/mindfulness-at-the-computer.desktop

"""

long_description_str = ""
# this_dir_abs_path_str = os.path.dirname(__file__)
readme_abs_path_str = os.path.join(setup_file_dir, "README.md")
try:
    with open(readme_abs_path_str, "r") as file:
        long_description_str = '\n' + file.read()
except FileNotFoundError:
    long_description_str = matc.constants.SHORT_DESCR

setup(
    name=matc.constants.APPLICATION_NAME,
    version=matc.constants.APPLICATION_VERSION,
    packages=['matc', 'matc.gui'],
    url="https://mindfulness-at-the-computer.gitlab.io",
    license='GPLv3',
    author='Tord Dellsén, and others',
    author_email=matc.constants.EMAIL_ADDRESS,
    description=matc.constants.SHORT_DESCR,
    include_package_data=True,
    install_requires=["PySide6>=6.2"],
    entry_points={"console_scripts": [f"{matc.constants.APPLICATION_NAME}=matc.main:main"]},
    long_description_content_type='text/markdown',
    long_description=long_description_str,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Other/Nonlisted Topic'
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
)

print("*********************************")
print(f"{setup_file_dir=}")
print(f"{appl_res_dir=}")
print("*********************************")

"""
Ubuntu versions and Python versions:
18.04 LTS: 3.6 - f-strings,
3.7 - 
20.04 LTS: 3.8 - 
21.04: 3.9 - 
22.04 - 3.10 - 

To install earlier versions:
https://www.digitalocean.com/community/questions/how-to-install-a-specific-python-version-on-ubuntu

https://www.python.org/downloads/
tar xzvf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install
https://askubuntu.com/a/727814/360991

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
https://askubuntu.com/a/682875/360991
Doesn't work for 3.6

List of classifiers:
https://pypi.org/classifiers/

"""
