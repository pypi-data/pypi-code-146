from typing import Dict, List, Tuple, Union

import yaml

from clutchGen.models import GenerationDirectory, GenerationFile


def read_file(path: str):
    with open(path, "r") as stream:
        endswith = path.endswith(".yaml")
        if endswith:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        else:
            raise NotImplementedError(path)


def parse(entry: Union[dict, str, list]):
    if isinstance(entry, dict):
        if len(entry) == 1 and list(entry.keys())[0] not in ("$filename", "$template", "$params"):
            item = list(entry.items())[0]
            dirname = item[0]
            return GenerationDirectory(dirname, nested=parse(item[1]))
        else:
            extra = set(entry.keys()) - {"$filename", "$template", "$params"}
            if extra:
                raise ValueError(f"Invalid params: {','.join(extra)}")
            return GenerationFile(
                name=entry.get("$filename"),
                template_name=entry.get("$template"),
                parameters=entry.get("$params"),
            )
    elif isinstance(entry, list):
        entries = [parse(value) for value in entry]
        return entries
    elif isinstance(entry, str):
        name, template_name = entry.split("$") if "$" in entry else (entry, None)
        return GenerationFile(name=name, template_name=template_name)


def parse_file(path: str) -> Tuple[List[Union[GenerationFile, GenerationDirectory]], Dict]:
    file_data = read_file(path)
    tree = parse(file_data["$root"])
    default_render_context = file_data.get("$defaultContext", {})
    return tree, default_render_context
