import sys
from setuptools import find_packages, setup

v = sys.version_info

install_requires = [line.strip() for line in open("requirements.txt")]

extra_args = {}

try:

    # enforce binary wheel on windows
    if sys.platform == "win32":
        from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

        class bdist_wheel(_bdist_wheel):
            def finalize_options(self):
                _bdist_wheel.finalize_options(self)
                self.root_is_pure = False

        extra_args["cmdclass"] = {"bdist_wheel": bdist_wheel}

except ImportError:
    pass


long_description = """
LCMS data analysis made easy

emzed is an open source toolbox for rapid and interactive development of LCMS data
analysis workflows in Python and makes experimenting with new analysis strategies for
LCMS data as easy as possible.
"""


setup(
    name="emzed-spyder",
    version="3.0.0a3",
    description="emzed IDE, see also https://emzed.ethz.ch",
    long_description=long_description,
    url="https://emzed.ethz.ch",
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["emzed.spyder.debug = emzed_spyder.start:main"],
        "gui_scripts": ["emzed.spyder = emzed_spyder.start:main"],
    },
    include_package_data=True,
    **extra_args,
)
