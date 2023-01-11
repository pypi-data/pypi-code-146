import os
import shutil
import subprocess

from distutils.command.build import build
from distutils.errors import CompileError
from setuptools import setup
from setuptools.dist import Distribution


class CustomBuild(build):
    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        native_dir = os.path.join(current_dir, 'native')

        res = subprocess.run(
            [
                'cargo',
                'build',
                '--features', 'c-api',
                '--release',
            ],
            cwd=native_dir,
            text=True,
        )

        if res.returncode != 0:
            raise CompileError("unable to build the native dependency")

        shutil.copy(
            os.path.join(native_dir, 'target', 'release', 'libgcdevproxy.so'),
            os.path.join(current_dir, 'gcdevproxy'),
        )

        return super().run()


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

setup(
    cmdclass={
        'build': CustomBuild,
    },
    distclass=BinaryDistribution,
)
