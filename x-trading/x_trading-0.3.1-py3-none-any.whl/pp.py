# x-trading
# Copyright 2023 Valmir França da Silva
# http://github.com/vfranca
import click
from x_trading._pp import pivot


# Cria o comando pp - ponto pivô
@click.command()
@click.argument("maxima", type=float)
@click.argument("minima", type=float)
@click.argument("fechamento", type=float)
def pp(maxima, minima, fechamento):
    """Calcula o ponto pivo."""
    pp = pivot.pp(maxima, minima, fechamento)
    click.echo(pivot.r2(pp, maxima, minima))
    click.echo(pivot.r1(pp, minima))
    click.echo(pp)
    click.echo(pivot.s1(pp, maxima))
    click.echo(pivot.s2(pp, maxima, minima))


if __name__ == "__main__":
    pp()
