from data_processing import PySmells
import click
import os

def centralize(word):
    print(f'{word:-^40}')

@click.command()
@click.option('--dir')
@click.option('--pylint', default=False)
@click.option('--pep8', default=False)
@click.option('--mypy', default=False)
def pysmell(dir, pylint, pep8, mypy):
    if pylint:
        os.system(f"pylint --msg-template='{{msg_id}}::{{msg}}' {dir} > pylint_errors.txt")

        centralize(' Pylint Errors ')
        print(PySmells('pylint_errors.txt').pylint_insigth())

        centralize(' Pylint Errors by Type ')
        print(PySmells('pylint_errors.txt').pylint_insigth(True))

        centralize(' Pylint Program Score ')
        print(PySmells('pylint_errors.txt').pylint_score())

    if pep8:
        os.system(f"pycodestyle --statistics -qq {dir} > pep8_errors.txt")

        centralize(' Pep8 Errors ')
        print(PySmells('pep8_errors.txt').pep8_insigth())

    if mypy:
        os.system(f"mypy --check-untyped-defs {dir} > mypy_errors.txt")

        centralize(' MyPy Errors ')
        print(PySmells('mypy_errors.txt').mypy_insigth())


if __name__ == '__main__':
    pysmell()
