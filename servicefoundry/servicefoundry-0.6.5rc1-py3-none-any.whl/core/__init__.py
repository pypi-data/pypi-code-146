from servicefoundry.core.login import login
from servicefoundry.core.logout import logout
from servicefoundry.core.notebook.notebook_util import is_notebook
from servicefoundry.core.requirements import gather_requirements

if is_notebook():
    try:
        import ipywidgets
    except ImportError:
        print("Run `pip install ipywidgets` to use notebook features.")

__all__ = [
    "login",
    "logout",
    "gather_requirements",
    "is_notebook",  # is this required?
]
