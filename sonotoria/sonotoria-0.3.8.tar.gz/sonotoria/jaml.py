# -*- coding: utf-8 -*-
from typing import Any, Dict, Callable
import yaml
from yaml.constructor import SafeConstructor

from . import jinja # pylint: disable=cyclic-import

def load(
    path: str,
    filters: Dict[str, Callable[[Any], Any]]  = None,
    tests:   Dict[str, Callable[[Any], bool]] = None,
    types:   Dict[str, object]                = None,
    context: Dict[str, Any]                   = None
) -> Any:
    """This function reads the file at the given path, templates it using jinja2 then returns the yaml data.

    Args:
        path: The path of the yaml file.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.
        types: A dict of objects to add to the template engine. Yaml tags as keys, objects as values.
        context: A dict with additional value for the context used when loading the yaml.

    Returns:
        The data contained in the templated yaml. Most probably a dict.

    Examples:
        >>> from sonotoria import jaml
        >>> data = jaml.load('my_file.yml')
    """
    with open(path, encoding='utf-8') as file:
        lines = file.read()
    return loads(lines, filters, tests, types, context)

def loads(
    yaml_content: str,
    filters: Dict[str, Callable[[Any], Any]]  = None,
    tests:   Dict[str, Callable[[Any], bool]] = None,
    types:   Dict[str, object]                = None,
    context: Dict[str, Any]                   = None
) -> Any:
    """This function reads the file at the given path, templates it using jinja2 then returns the yaml data.

    Args:
        yaml_content: The yaml as a string.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.
        types: A dict of objects to add to the template engine. Yaml tags as keys, objects as values.
        context: A dict with additional value for the context used when loading the yaml.

    Returns:
        The data contained in the templated yaml. Most probably a dict.

    Examples:
        >>> from sonotoria import jaml
        >>> jaml.loads('---\nparam: value\nparam2: {{ param }}')
        {'param': 'value', 'param2': 'value'}
    """
    for tag, type_ in (types or {}).items():
        _add_data_type(tag, type_)

    current_context = {}

    content = []
    for line in yaml_content.split('\n'):
        if '{{' not in line:
            content.append(line)
        else:
            current_context = yaml.safe_load('\n'.join(content))
            content.append(
                jinja.template_string(
                    line,
                    merge_context(current_context, context),
                    filters = filters or {},
                    tests = tests or {}
                )
            )

    return yaml.safe_load('\n'.join(content))

def dumps(data: Any):
    """This function dumps the given data in a yaml representation string.

    Args:
        data: The data.

    Returns:
        A yaml representation string of the data.

    Examples:
        >>> from sonotoria import jaml
        >>> jaml.dumps({'foo': 'bar'})
        'foo: bar\n'
    """
    return yaml.dump(data, Dumper=IndentedDumper, default_flow_style=False)

def dump(file: str, data: Any):
    """This function dumps the given data in a yaml representation file.

    Args:
        data: The data.
        file: Path to file to be created.

    Examples:
        >>> from sonotoria import jaml
        >>> jaml.dump('dump.yaml', {'foo': 'bar'})
    """
    with open(file, encoding='utf-8', mode='w') as fd:
        fd.write(dumps(data))

def mapping_to_dict(mapping):
    """This function is to be used in the construct function of a loaded object.
    It takes a MappingNode object and return its content in the form of python dict.

    Args:
        mapping: A MappingNode object.

    Examples:
        >>> from sonotoria.jaml import mapping_to_dict
        >>> class MyObject:
        >>>     def construct(self, data): # do not use self, it won't be your object
        >>>         data = mapping_to_dict(data)
    """
    content = yaml.constructor.MappingNode('tag:yaml.org,2002:map', mapping.value)
    return SafeConstructor().construct_mapping(content, deep=True)

class MappedObject: #pylint: disable=too-few-public-methods
    @classmethod
    def constructor(cls):
        def construct(_, data):
            return cls(mapping_to_dict(data))
        return construct

class IndentedDumper(yaml.Dumper): #pylint: disable=too-many-ancestors
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def merge_context(context1, context2):
    if isinstance(context1, dict) and isinstance(context2, dict):
        return { **context1, **context2 }
    if isinstance(context2, dict) and context1 is None:
        return context2
    return context1

def ordered(class_):
    yaml.add_representer(class_, _represent_ordered)
    return class_

def constructed(class_):
    yaml.SafeLoader.add_constructor(class_.yaml_tag, class_.constructor())

def _represent_ordered(dumper, data):
    return yaml.nodes.MappingNode(
        data.yaml_tag,
        [
            (
                dumper.represent_data(key),
                dumper.represent_data(getattr(data, key))
            )
            for key in data.attr_order
        ]
    )

def _add_data_type(tag, class_):
    class_.yaml_tag = f'!{tag}'
    try:
        constructed(class_)
    except AttributeError:
        class_.yaml_loader = yaml.SafeLoader
        new_class = type(f'Yaml{class_.__name__}', (yaml.YAMLObject,), {k: v for k, v in class_.__dict__.items() if not k.startswith('__')})
        if hasattr(new_class, 'attr_order'):
            ordered(new_class)
