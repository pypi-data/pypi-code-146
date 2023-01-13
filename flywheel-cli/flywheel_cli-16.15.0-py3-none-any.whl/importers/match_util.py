"""Tools for extracting metadata from strings"""
import re
from typing import Pattern

from .. import util


def extract_metadata_attributes(name, template, context):
    """Extracts metadata from name using the given template.

    Stores any extracted metadata in context.

    Params:
        name (str): The file or folder name (without extension)
        template (str|Pattern): The extraction pattern.
        context (dict): The context to update

    Returns:
        bool: True if the pattern matched, otherwise False
    """
    groups = {}

    if isinstance(template, Pattern):  # pylint: disable=W1116
        match = template.match(name)
        if not match:
            return False
        groups = match.groupdict()
    else:
        groups[template] = name

    for key, value in groups.items():
        if value:
            key = util.python_id_to_str(key)
            if key in util.METADATA_ALIASES:
                key = util.METADATA_ALIASES[key]

            if key in util.METADATA_FUNC:
                value = util.METADATA_FUNC[key](value)

            util.set_nested_attr(context, key, value)

    return True


def compile_regex(value):
    """Compile a regular expression from a template string

    Args:
        value (str): The value to compile

    Returns:
        Pattern: The compiled regular expression
    """
    regex = ""
    escape = False
    repl = ""
    in_repl = False
    for char in value:
        if escape:
            regex = regex + "\\" + char
            escape = False
        else:
            if char == "\\":
                escape = True
            elif char == "{":
                in_repl = True
            elif char == "}":
                in_repl = False
                if _is_property(repl):
                    # Known FW metadata field like project.label - replace w/ group
                    regex = regex + f"(?P<{repl}>{util.regex_for_property(repl)})"
                elif re.match(r"\d+(,(/d+)?)?", repl):
                    # Additionally allow simple regex repetitions
                    regex = regex + "{" + repl + "}"
                else:
                    # But nothing else (ie. path cannot contain {})
                    raise ValueError(f"Invalid template pattern {repl} in {value}")
                repl = ""
            elif in_repl:
                repl = repl + char
            else:
                regex = regex + char

    # Finally, replace group ids with valid strings
    regex = re.sub(r"(?<!\\)\(\?P<([^>]+)>", _group_str_to_id, regex)
    return re.compile(regex)


def _is_property(value):
    if value in util.METADATA_FIELDS or value in util.METADATA_ALIASES:
        return True
    return any(value.startswith(f"{level}.info.") for level in util.METADATA_ALIASES)


def _group_str_to_id(match):
    return f"(?P<{util.str_to_python_id(match.group(1))}>"
