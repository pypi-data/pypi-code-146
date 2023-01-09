import os

from clutchGen.configs import delete_default_filename, delete_template_file, get_template_file
from clutchGen.constants import TEMPLATES_PATH


def handle_delete_template(template_name: str) -> None:
    os.remove(f"{TEMPLATES_PATH}/{get_template_file(template_name)}")
    delete_template_file(template_name)
    delete_default_filename(template_name)
