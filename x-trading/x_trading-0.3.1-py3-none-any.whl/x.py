# x-trading
# Copyright 2023 Valmir França da Silva
# http://github.com/vfranca
import click
from x_trading import __version__


# Importa os comandos
from x_trading.pp import pp
from x_trading.vp import vp


# Cria o grupo de comandos x
@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True)
def x(version):
    """Grupo de comandos para calculos no day trading."""
    if version:
        click.echo("x-trading %s" % __version__)


# Adiciona os comandos
x.add_command(pp)
x.add_command(vp)


if __name__ == "__main__":
    x()
