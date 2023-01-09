import os
import shutil

from clutchGen.configs import (
    delete_default_filename,
    delete_template_file,
    get_default_file_name,
    get_template_file,
    set_default_filename,
    set_template_file,
)
from clutchGen.constants import TEMPLATES_PATH


def handle_edit_template(template_name: str, field, value):
    if field == "file":
        os.remove(f"{TEMPLATES_PATH}/{get_template_file(template_name)}")
        delete_template_file(template_name)
        shutil.copy(value, TEMPLATES_PATH)
        set_template_file(template_name, value)
    elif field == "name":
        file = get_template_file(template_name)
        default_name = get_default_file_name(template_name)
        delete_template_file(template_name)
        delete_default_filename(template_name)
        set_template_file(template_name, file)
        set_default_filename(template_name, default_name)
    elif field == "default-name":
        set_template_file(template_name, value)
