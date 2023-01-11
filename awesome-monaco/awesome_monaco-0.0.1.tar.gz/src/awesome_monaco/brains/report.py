from brains.build_data import RacerInfo
from brains.config import limit, line_length


def print_report(report: {str: RacerInfo}, reverse=True):
    """Проблемма не в двух словарях а как правильно Reverce реализовывать"""
    spacer = check_max_string_length(report)
    racers = list(report.values())

    before_line = racers[:limit]
    after_line = racers[limit:]

    if reverse:
        before_line = racers[:-limit]
        after_line = racers[-limit:]

    for racer in before_line:
        racer.print(spacer)

    print("_" * line_length)

    for racer in after_line:
        racer.print(spacer)


def check_max_string_length(reports):
    """find max length of racer name + command
    used to build the same length of strings in build_total_print"""

    max_length = max(reports.values(), key=lambda i: len(i.name) + len(i.team))
    max_length = len(max_length.team) + len(max_length.name)

    max_length = max([len(report.name) + len(report.team) for report in reports.values()])
    return max_length + 1
