"""@Author: Rayane AMROUCHE

Report view functions.
"""

import os
from typing import Any


def view_eda_report(report: Any, dir_path: str, report_name: str) -> None:
    """Save an html eda report from a given report.

    Args:
        report (Any): Report to save as an html.
        dir_path (str): Directory path of the html report to save.
        report_name (str): Name of the html report to save.
    """
    os.makedirs(dir_path, exist_ok=True)
    report.show_html(os.path.join(dir_path, report_name))
