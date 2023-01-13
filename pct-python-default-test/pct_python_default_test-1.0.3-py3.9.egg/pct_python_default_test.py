# STDLIB
import sys


# main{{{
def main() -> None:
    """
    the main method, prints hello world


    Parameter
    ----------
    none
        none


    Result
    ----------
    none


    Exceptions
    ----------
    none


    Examples
    ----------

    >>> main()
    Hello World - by PizzaCutter

    """
    # main}}}

    print("Hello World - by PizzaCutter")


if __name__ == "__main__":
    print(b'this is a library only, the executable is named "pct_python_default_test_cli.py"', file=sys.stderr)
