from typing import List, Tuple

from norma2.config.config_class import Config
from norma2.errors.norm import Severity, _TemplateNormError


def get_sort_diff_err(
    errs: List[List[_TemplateNormError]],
) -> List[List[_TemplateNormError]]:
    new: List[List[_TemplateNormError]] = []
    types: List[_TemplateNormError] = []
    for _errs in errs:
        for err in _errs:
            added = False
            for i, _type in enumerate(types):
                if type(_type) is type(err):
                    added = True
                    new[i].append(err)
            if not added:
                new.append([err])
                types.append(err)
    return new


def get_avverage_file(errs: List[List[_TemplateNormError]]) -> float:
    nb_err_per_file = [len(x) for x in errs]
    return round(sum(nb_err_per_file) / len(nb_err_per_file), 2)


def get_stat_severity(errs: List[List[_TemplateNormError]]) -> Tuple[int, int, int]:
    nb_major = 0
    nb_minor = 0
    nb_info = 0

    for _errs in errs:
        for err in _errs:
            if err.severity == Severity.MAJOR:
                nb_major += 1
            elif err.severity == Severity.MINOR:
                nb_minor += 1
            elif err.severity == Severity.INFO:
                nb_info += 1
    return nb_major, nb_minor, nb_info


def get_color(val) -> str:
    if val == 0:
        return f"[green]{val}"
    return f"[red]{val}"


def show_stat_folder(
    folder: str, config: Config, errs: List[List[_TemplateNormError]]
):  # noqa: E501
    if config.only_exit_code:
        return
    diff = get_sort_diff_err(errs)
    err_avvr_file = get_avverage_file(errs)
    nb_major, nb_minor, nb_info = get_stat_severity(errs)
    s_major, s_minor, s_info = nb_major * -3, nb_minor * -1, 0
    score = s_major + s_minor + s_info
    config.console.print(f"[blue]Stats: {folder}", justify="center")
    config.console.print(f"- Number of Different Errors: {get_color(len(diff))}")
    config.console.print(
        f"- Averrage Number of Errors per File: {get_color(err_avvr_file)}"
    )
    config.console.print(
        f"- Number of MAJOR: {get_color(nb_major)} " f"({get_color(s_major)})"
    )
    config.console.print(
        f"- Number of MINOR: {get_color(nb_minor)} " f"({get_color(s_minor)})"
    )
    config.console.print(
        f"- Number of INFO: {get_color(nb_info)} " f"({get_color(s_info)})"
    )
    config.console.print(f"- Your score: {get_color(score)}")
