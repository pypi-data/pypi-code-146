def args_dict_to_str(args: dict[str, str]) -> str:
    args_str_list = [
        "{0}={1}".format(key, value) for key, value in args.items()
    ]
    return ", ".join(args_str_list)
