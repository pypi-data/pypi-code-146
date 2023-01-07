"""@Author: Rayane AMROUCHE

Report view functions.
"""

import os
from typing import Any

import explainerdashboard as ed  # type: ignore


def view_shap_explainer(explainer: Any) -> None:
    """Launch a flask dash server of an explainer dashboard.

    Args:
        explainer (Any): Explainer to display.
    """
    ed.ExplainerDashboard(explainer).run()


def view_eda_report(report: Any, dir_path: str, report_name: str) -> None:
    """Save an html eda report from a given report.

    Args:
        report (Any): Report to save as an html.
        dir_path (str): Directory path of the html report to save.
        report_name (str): Name of the html report to save.
    """
    os.makedirs(dir_path, exist_ok=True)
    report.show_html(os.path.join(dir_path, report_name))
