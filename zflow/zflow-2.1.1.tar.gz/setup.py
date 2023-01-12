from setuptools import setup
from setuptools.command.install import install
import os
import sys

# Regular import isn't working, so we open __version__.py and evaluate it
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "__version__.py")) as version_file:
    version_data = version_file.read()
exec(version_data)

INSTALL_URL = f"git+ssh://git@github.bus.zalan.do/zai/zflow.git@{__version__}#egg=zflow"  # noqa: F821


class PostInstallCommand(install):
    def run(self):
        status = os.system(f"pip install {INSTALL_URL}")
        if status == 0:
            print("zflow installed successfully.")
        print(
            "WARNING: installing zflow from pypi.org will soon be deprecated.\n"
            "Please install zflow from internal Zalando sources.\n"
            "Refer to zflow documentation for up-to-date instructions."
        )
        sys.exit(status)


setup(
    author="Zalando SE",
    author_email="zflow-team@gmail.com",
    description="Zalando zflow installer",
    install_requires=[],
    license="MIT license",
    cmdclass={
        "install": PostInstallCommand,
    },
    include_package_data=True,
    keywords="zflow",
    name="zflow",
    py_modules=["__version__"],
    setup_requires=[],
    tests_require=[],
    url="https://github.bus.zalan.do/zai/zflow",
    version=__version__,  # noqa: F821
    zip_safe=False,
)
