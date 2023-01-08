import argparse

import privateprefs.core.database as _db


def _save_cli(key: str, value: str) -> None:
    """
    Saves the value for a given key.
    :param key: A unique key to write the value under
    :param value: The value to be save into persistent storage
    :return: None
    """
    _db.write(key, value)
    print(f"saved value: '{value}'")


def _load_cli(key: str) -> None:
    """
    Loads and returns the value for a given key
    :param key: A key to read the value of
    :return: None
    """
    value = _db.read(key)
    print(f"loaded value: '{value}'")


def _delete_cli(key: str = None, delete_all: bool = False) -> None:
    """


    :param key: A key that will be used to delete the corresponding key-value pair
    :return: None

    Deletes a key-value pair, or deletes all stored key-value pairs.
    :param key: The key to be deleted
    :param delete_all: If flag is true, all key-value pairs will be deleted
    :return: None
    """
    if delete_all:
        _db.delete_all()
        print(f"all key-value pairs deleted")
    else:
        print(f"deleted value: '{_db.read(key)}'")
        _db.delete(key)


def _list_cli() -> None:
    """
    Displays a table of all saved key-value pairs.
    :return: None
    """
    print_key_value_table()


def print_key_value_table() -> None:
    """
    Prints out a table of all saved key-value pairs.
    :return: None
    """
    print()
    key_value_pairs = _db.read_keys()

    if len(key_value_pairs) > 0:
        max_len_key = max(len(x) for x in key_value_pairs.keys())
        max_len_value = max(len(x) for x in key_value_pairs.values())
        max_len_key = max(max_len_key, 10)
        max_len_value = max(max_len_value, 10)
    else:
        max_len_key = 10
        max_len_value = 11
        key_value_pairs["   ...   "] = "    ...   "
        print("- no key-value pairs saved -".lower())

    key_blank = "-" * max_len_key
    value_blank = "-" * max_len_value

    key_header_centered = f'{"KEY":^{max_len_key}s}'
    value_header_centered = f'{"VALUE":^{max_len_value}s}'
    print(f"+-{key_blank}-+-{value_blank}-+")
    print(f"| {key_header_centered} | {value_header_centered} |")
    print(f"+-{key_blank}-+-{value_blank}-+")

    for key, val in key_value_pairs.items():
        key = key.ljust(max_len_key)
        val = val.ljust(max_len_value)
        print(f"| {key} | {val} |")

    print(f"+-{key_blank}-+-{value_blank}-+")
    print()


def main(argv=None) -> None:
    """
    This main function is the entry point for our CLI in our package.

    In the project.toml file under [project.scripts] is a line code that invokes
    this method. This method instantiate argparse and instantiates sub-commands
    then dynamically calls the function associated with the subcommand been called.
    :param argv: Injected arguments when running unit tests, and None when cli used
    from the command line
    :return: None
    """

    # Instantiate argparse and a subparsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    # To make argparse sub-parsers easier to deal with, we set up one function per subparsers.

    # The Save sub-parsers.
    # A function called 'save_' will be dynamically called when the 'save' command is invoked
    parser_save = subparsers.add_parser("save")
    parser_save.add_argument("key")
    parser_save.add_argument("value")

    # The Load sub-parsers.
    # A function called 'load_' will be dynamically called when the 'load' command is invoked
    parser_load = subparsers.add_parser("load")
    parser_load.add_argument("key")

    # The List sub-parsers.
    # A function called 'list_' will be dynamically called when the 'list' command is invoked
    subparsers.add_parser("list")

    # The Delete sub-parsers.
    # A function called 'delete_' will be dynamically called when the 'delete' command is invoked
    # Note that only the 'key' or '--all' argument is required, depending on if we want to delete
    # single key-value pair or all key-value pairs.
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument('key', nargs='?')
    parser_delete.add_argument("--all",
                               dest="delete_all",
                               action="store_true")
    args = parser.parse_args(argv)
    no_args_given = args.subparser == "delete" and args.key is None and args.delete_all is False
    if no_args_given:
        raise parser.error("you must enter a key string argument or enter the '--all' flag")

    # Extract a dict containing the name of the sub processor invoked and its arguments
    kwargs = vars(parser.parse_args(argv))

    # Extract the name of the subcommand being invoked, note we pop/remove the subcommand name,
    # so now kwargs will be just the given arguments without the subcommand in the dict.
    func_name_to_call = kwargs.pop('subparser')  # will be: save, load, delete, etc.

    # The private cli functions start with an underscore and end with _cli, so we append it here.
    # E.g. if we called 'save' in the cli, here it would become '_save_cli' to match the function name.
    func_name_to_call = f"_{func_name_to_call}_cli"

    # We dynamically call the function from the globals namespace dictionary and pass in cli the arguments.
    globals()[func_name_to_call](**kwargs)


if __name__ == '__main__':
    main()
