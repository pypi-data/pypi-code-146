import subprocess
from setuptools import Extension, setup
from distutils.errors import CompileError
from distutils.command.build_ext import build_ext

ext_modules = [
    Extension("cdncheck", ["cdncheck.go"])
]

class build_go_ext(build_ext):
    """Custom command to build extension from Go source files"""

    def build_extension(self, ext):
        ext_path = self.get_ext_fullpath(ext.name)
        cmd = ["go", "build", "-buildmode=c-shared", "-o", ext_path]
        print(f"Running {' '.join(cmd)}")
        cmd += ext.sources
        try:
            out = subprocess.run(cmd, check=True)
        except Exception as e:
            raise CompileError(f"Go build failed. Please ensure golang is installed. ({e})")


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": ext_modules, "cmdclass": {"build_ext": build_go_ext}}
    )
