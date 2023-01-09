import os

from mako.lookup import TemplateLookup

from clutchGen.configs import get_default_file_name, get_template_file
from clutchGen.constants import TEMPLATES_PATH
from clutchGen.models import GenerationFile
from clutchGen.render_context import get_render_context

templates = TemplateLookup(directories=[TEMPLATES_PATH])


def render_template(file: GenerationFile, path: str = ""):
    file_name, template = (
        file.name or get_default_file_name(file.template_name),
        get_template_file(file.template_name),
    )
    content = templates.get_template(template).render(**get_render_context(file.parameters)) if template else ""
    if path and not os.path.exists(path):
        os.makedirs(path)
    with open(f"{path}/{file_name}" if path else file_name, "w+") as f:
        f.write(content)
