"""Setup script for victorforever"""

import os.path
from setuptools import setup
from setuptools.command.install import install

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        try:
            import webbrowser
            webbrowser.open("https://youtu.be/xvFZjo5PgG0")
        except:
            pass

        print("\n")
        print("##############################################")
        print("#                VICTOR FOREVER              #")
        print("##############################################")
        print("\n")

# This call to setup() does all the work
setup(
    name="victorforever",
    version="1.0.1",
    description="Victor Forever",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://youtu.be/xvFZjo5PgG0",
    author="Ward Van Driessche",
    author_email="wardvandriessche@gmail.com",
    cmdclass={
        'install': PostInstallCommand,
    },
    packages=["victorforever"],
    include_package_data=False,
    install_requires=[],
    entry_points={"console_scripts": ["victorforever=victorforever:main"]},
)
