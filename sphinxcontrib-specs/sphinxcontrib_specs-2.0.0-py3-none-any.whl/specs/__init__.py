from os import path
from pathlib import Path

from sphinx.application import Sphinx

from . import builder, content, objectives, steps, overridenodes

package_dir = Path(path.abspath(path.dirname(__file__)))


def setup(app: Sphinx) -> None:
    # Theme
    app.add_html_theme("specs", str((package_dir / "theme").resolve()))

    # Static files
    app.add_css_file(
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css",
        0,
    )
    app.add_js_file(
        "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.5/dist/umd/popper.min.js"
    )
    app.add_js_file(
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.min.js"
    )

    # Contentlist extension
    content.setup(app)

    # Objectives extension
    objectives.setup(app)

    # Steps extension
    steps.setup(app)

    overridenodes.setup(app)
