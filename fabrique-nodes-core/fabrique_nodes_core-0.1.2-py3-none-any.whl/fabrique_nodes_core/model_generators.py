from pathlib import Path
import json
import os
from pydantic import BaseModel
import typing
from datamodel_code_generator import InputFileType, generate
# import importlib
from importlib.machinery import SourceFileLoader
from fabrique_nodes_core.core import Port

cur_file_dir = os.path.dirname(os.path.abspath(__file__))


def data2models(data, input_file_type=InputFileType.Auto, path='.'):
    """Generate and import model from object/array data

    :param data: object/array data
    :param input_file_type: convert param, defaults to InputFileType.Auto
    :type input_file_type: str, optional
    :param path: path to file
    :type path: str, optional
    :return: data model of "data" in module
    :rtype: ModuleType
    """
    output = Path(os.path.join(path, 'model.py'))
    full_pth = str(output)
    generate(
        data,
        input_file_type=input_file_type,
        input_filename="example.json",
        output=output,
    )
    model = SourceFileLoader('model', full_pth).load_module()
    try:
        os.remove(full_pth)
    except OSError:
        pass
    return model


def jsons2model(jsons: typing.List[str], input_file_type=InputFileType.Json, path='.') -> BaseModel:
    """Converts jsons to data model

    :param jsons: json examples list for model generation
    :type jsons: typing.List[str]
    :param input_file_type: convert param, defaults to InputFileType.Json
    :param path: path to file
    :type path: str, optional
    :return: data model of jsons in BaseModel
    :rtype: BaseModel
    """
    jsons_str = ',\n'.join(jsons)
    json_data = f"[{jsons_str}]"
    model = data2models(json_data, input_file_type, path)
    return model.ModelItem


def schema2model(json_schema: str) -> BaseModel:
    """Converts json_schema to data model

    :param json_schema: json schema to convert
    :type json_schema: str
    :return: data model of schema
    :rtype: BaseModel
    """
    py_dict = json.loads(json_schema)
    py_dict.pop('title', 0)
    schema = json.dumps(py_dict)
    model = data2models(schema, input_file_type=InputFileType.JsonSchema)
    return model.Model


def model2schema(model: BaseModel) -> str:
    """Converts model to schema

    :param model: data model to convert
    :type model: BaseModel
    :return: json schema
    :rtype: str
    """
    py_dict = model.schema()
    py_dict.pop('title', 0)
    return json.dumps(py_dict, indent=2)


def field2schema(model: BaseModel, field_name: str) -> str:
    """_summary_

    :param model: _description_
    :type model: BaseModel
    :param field_name: _description_
    :type field_name: str
    :return: _description_
    :rtype: str
    """
    type_ = model.__fields__[field_name].type_
    return model2schema(type_)


def is_list(field_cls) -> bool:
    """Checks if field_cls is list

    :param field_cls: instance to check
    :return: result
    :rtype: bool
    """
    return typing.get_origin(field_cls.outer_type_) is list


def is_object(field_cls) -> bool:
    """Checks if field_cls is dict

    :param field_cls: instance to check
    :return: result
    :rtype:
    """
    type_ = field_cls.type_
    return issubclass(type_, BaseModel)


def model2ports(Model: BaseModel) -> typing.List[Port]:
    """Generate ports from Model

    :param Model: node data model
    :type Model: BaseModel
    :return: list of generated ports
    :rtype: typing.List[Port]
    """
    model_type = dict
    if Model.__fields__.get('__root__'):
        model_type = list
    model_port = Port(id_='root', name='root', special=True)
    model_port.type_ = model_type
    model_port.schema_ = model2schema(Model)

    def field2port(key, val):
        code = key
        type_ = val.type_
        port = Port(id_=key, name=key)
        port.required = Model.__fields__[key].required
        port.code = code
        if is_list(val):
            port.type_ = list
            if is_object(val):
                port.schema_ = model2schema(type_)
        elif is_object(val):
            port.type_ = dict
            port.schema_ = model2schema(type_)
        else:
            port.type_ = type_
        return port

    # ports = [ model2port('root', Model), ]

    ports = [model_port, ] + [field2port(key, val) for key, val in Model.__fields__.items()]
    return ports
