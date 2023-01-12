import typing
from pathlib import Path

import click

from ...utils.cache import export, open_cache
from ...utils.run import run


@click.command()
@click.option(
    "--llvm-home",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=False,
)
def main(llvm_home: typing.Optional[str | Path] = None) -> None:
    with open_cache() as cache:
        env: dict[str, str] = dict()
        if llvm_home:
            llvm_config = Path(llvm_home) / "bin" / "llvm-config"
        else:
            llvm_config = "llvm-config"
        completed_process = run(str(llvm_config), "--libdir", capture_output=True)
        lib_dir = str(completed_process.stdout, encoding="utf-8").strip()
        env["LD_LIBRARY_PATH"] = lib_dir + ":"
        export(cache=cache, env=env)
