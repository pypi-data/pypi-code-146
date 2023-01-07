from typing import List

from norma2.checkers.check import check as check_norm
from norma2.config.config_class import Config
from norma2.config.from_gitignore import from_gitignore
from norma2.errors.norm import ALL_ERROR_NORM, _TemplateNormError
from norma2.parser import file, get_files
from norma2.show_stats import show_stat_folder


def print_header(config: Config):
    if not config.only_exit_code:
        config.console.rule("[bold blue]norma2", style="bold blue")
        config.console.print("Check the Epitech C Coding Style", style="italic")
        config.console.line(2)


def print_config(config: Config):
    if config.show_config:
        config.console.rule("Parsed Config from cmdline + `.norma2.json`", style="blue")
        config.console.print_json(data=config.to_dict())
        config.console.line()


def check_file(config, filepath: str) -> List[_TemplateNormError]:
    list_err: List[_TemplateNormError] = []
    if not config.only_exit_code:
        config.console.print(f"[magenta underline]{filepath}")
    try:
        f = file.File(filepath, config)
        f.init()
        list_err = f.check_norm()
        list_err.extend(check_norm(f))
    except Exception:
        config.console.print(":warning: [red]An Error Occured")
        config.console.print_exception()
    else:
        if not config.only_exit_code and list_err:
            list_to_print = list(
                map(
                    lambda x: x.show(
                        with_explanation=config.show_explanation, print_stdout=False
                    ),
                    list_err,
                )
            )
            to_print = "\n".join(list_to_print)
            config.console.print(to_print)
    if not config.only_exit_code:
        if not list_err:
            config.console.print("FILE [green]OK :heavy_check_mark:")
        else:
            config.console.print("FILE [red]KO x")
        config.console.line()
    return list_err


def print_footer(config: Config):
    if not config.only_exit_code:
        config.console.print(f"Time: {config.console.get_datetime()}", justify="right")


def explain_error(err: str, config: Config) -> int:
    at_least = False
    for norm in ALL_ERROR_NORM:
        if err in norm.rule:
            at_least = True
            to_print = norm.only_explanation(print_stdout=False)
            config.console.print(to_print)
    if at_least:
        return 0
    config.console.print("[red]No norm error with this code")
    return 2


def list_errors(config: Config):
    for norm in ALL_ERROR_NORM:
        to_print = norm.only_explanation(print_stdout=False)
        config.console.print(to_print)


def main(config: Config) -> int:
    nb_errors = 0
    print_header(config)
    print_config(config)

    if config.pass_test:
        print("Not implemented yet")
        return 0

    if config.explain_error:
        return explain_error(config.explain_error, config)

    if config.list_errors:
        list_errors(config)
        return 0

    if not config.only_exit_code:
        config.console.rule("Norm:", style="blue")
    for folder in config.paths:
        if not config.only_exit_code:
            config.console.line()
            config.console.print(f"[blue]Check: {folder}", justify="center")
        list_all_err: List[List[_TemplateNormError]] = []
        try:
            conf_gitignore = from_gitignore(config.console, folder)
            files_to_check = get_files.get_all_files(
                folder,
                config.folder_exclude,
                config.file_ext_exclude,
                conf_gitignore.gitignore_matches,
            )
        except Exception:
            config.console.print(":warning: [red]An Error Occured")
            config.console.print_exception()
            continue
        for filepath in files_to_check:
            list_all_err.append(check_file(config, filepath))
            nb_errors += len(list_all_err[-1])
        show_stat_folder(folder, config, list_all_err)

    print_footer(config)
    if nb_errors:
        return 42
    return 0
