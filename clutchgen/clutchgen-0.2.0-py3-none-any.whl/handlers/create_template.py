import shutil
from typing import Optional

from clutchGen.configs import set_default_filename, set_template_file
from clutchGen.constants import TEMPLATES_PATH


def handle_create_template(file: str, template_name: str, generation_name: Optional[str] = "") -> None:
    shutil.copy(file, TEMPLATES_PATH)
    set_template_file(template_name, file)
    if generation_name:
        set_default_filename(template_name, generation_name)
