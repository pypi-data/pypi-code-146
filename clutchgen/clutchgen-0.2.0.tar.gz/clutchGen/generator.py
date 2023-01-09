from typing import List, Union

from .models import GenerationDirectory, GenerationFile
from .templating import render_template


def generate_structure(
    obj: Union[List[Union[GenerationDirectory, GenerationFile]], GenerationFile, GenerationDirectory], path: str = ""
) -> None:
    if type(obj) == GenerationFile:
        render_template(obj, path)
    elif type(obj) == GenerationDirectory:
        generate_structure(obj.nested, f"{path}/{obj.name}" if path else obj.name)
    elif type(obj) == list:
        for i in obj:
            generate_structure(i, path)
    else:
        raise NotImplementedError("Not implemented")
