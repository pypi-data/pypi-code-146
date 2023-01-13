from . import __name__ as pkgname
from .cli import cli

if __name__ == "__main__":
    cli(prog_name=pkgname)
