# polygon/__main__.py

from polygon import cli, __app_name__, dataset, container, search

def main():
    cli.app(prog_name=__app_name__)
    # dataset.app(prog_name=__app_name__)
    # container.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()