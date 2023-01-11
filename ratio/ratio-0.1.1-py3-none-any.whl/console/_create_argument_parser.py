import argparse


def _create_argument_parser() -> argparse.ArgumentParser:
    main_parser = argparse.ArgumentParser(
        conflict_handler="resolve",
        allow_abbrev=False,
        add_help=False,
        exit_on_error=False,
    )
    main_parser.add_argument("command")

    return main_parser
