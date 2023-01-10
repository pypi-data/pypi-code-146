import os
import re
import string
from pathlib import Path
from typing import List

import libcst as cst
from datamodel_code_generator import PythonVersion
from datamodel_code_generator.format import CodeFormatter

from .cst import BaseCST
from .utils import validation

base_cst = BaseCST()


class ClassGenerator(BaseCST):
    def __init__(self, data: List[dict]) -> None:
        self.classname: str = data.get('name')
        self.description: str = data.get('description')
        self.base_classes: List[str] = data.get('base_classes')
        self.class_attributes: dict = data.get('attributes')
        self.instance_attributes: dict = data.get('instance_attributes')
        self.instance_methods: dict = data.get('instance_methods')

    @property
    def class_name(self) -> str:
        name = re.sub(r"[^a-zA-Z0-9 ]", "", self.classname)
        name = name.translate({ord(c): None for c in string.whitespace})
        return name.capitalize()

    @property
    def class_description_CST(self) -> List[cst.SimpleStatementLine]:
        description: str = f"'''\n    {self.description}\n    '''"
        body = cst.Expr(value=cst.SimpleString(description))
        return [cst.SimpleStatementLine(body=[body])]

    @property
    def bases_class_CST(self) -> List[cst.Arg]:
        bases: List[cst.Arg] = []
        for base_class in self.base_classes:
            arg = cst.Arg(cst.Name(str(base_class)))
            bases.append(arg)
        return bases

    @property
    def class_attributes_CST(self) -> List[cst.SimpleStatementLine]:
        fields: List[cst.SimpleStatementLine] = []
        for attr in self.class_attributes:
            ann_assign = self.create_class_attr_CST(
                str(attr.get('name')), str(attr.get('value')), str(attr.get('type')))
            fields.append(ann_assign)
        return fields

    @property
    def instance_attributes_CST(self) -> List[cst.FunctionDef]:
        class_method_attrs: List[cst.SimpleStatementLine] = []
        method_name: cst.Name = cst.Name(self.class_name.lower() + '_method')

        for attr in self.instance_attributes:
            class_method_attrs.append(
                self.create_instance_attr_CST(str(attr.get('name')), str(attr.get('value')))
            )
        body = cst.IndentedBlock(body=class_method_attrs)
        return [cst.FunctionDef(
            name=method_name,
            params=cst.Parameters(params=[cst.Param(cst.Name('self'))]),
            body=body,
            decorators=[],
            returns=None
        )]

    @property
    def class_getter_methods_CST(self) -> List[cst.FunctionDef]:
        getters: List[cst.FunctionDef] = []
        for attr in self.instance_attributes:
            getters.append(self.create_getter_CST(str(attr.get('name')), str(attr.get('type'))))
        return getters

    @property
    def class_setter_methods_CST(self) -> List[cst.FunctionDef]:
        setters: List[cst.FunctionDef] = []
        for attr in self.instance_attributes:
            setters.append(self.create_setter_CST(str(attr.get('name')), str(attr.get('type'))))
        return setters

    @property
    def instance_methods_CST(self) -> List[cst.FunctionDef]:
        methods_cst: List[cst.FunctionDef] = []
        for method in self.instance_methods:
            if method.get('definition'):
                method_cst = self.create_instance_method_CST(
                    method['definition'].get('name'),
                    method['definition'].get('decorators'),
                    method['definition'].get('arguments'),
                    method['definition'].get('statements'),
                    method['definition'].get('return_type')
                )
            else:
                method_cst = self.get_node_from_git(
                    method['github'].get('url'),
                    method['github'].get('filename'),
                    method['github'].get('target'),
                    True
                )
            if method_cst:
                methods_cst.append(method_cst)
        return methods_cst

    def make_cst(self) -> cst.ClassDef:
        class_name = cst.Name(self.class_name)
        class_body = (
            self.class_description_CST + self.class_attributes_CST
            + self.instance_attributes_CST + self.class_getter_methods_CST
            + self.class_setter_methods_CST + self.instance_methods_CST
        )
        base_classes = self.bases_class_CST
        return cst.ClassDef(
            name=class_name,
            body=cst.IndentedBlock(body=class_body),
            bases=base_classes
        )


class StatementGenerator(BaseCST):
    def make_cst(self, data: List[str]) -> List[cst.SimpleStatementLine]:
        imports_cst: List[cst.SimpleStatementLine] = []
        for statement in data:
            import_CST = self.create_import_CST(statement)
            imports_cst.append(import_CST)
        return imports_cst


class DataStructureGenerator(BaseCST):
    def make_cst(self, data: List[dict]) -> List[cst.Element]:
        data_structres_cst = []
        for d in data:
            data_structres_cst.append(self.create_data_structure_CST(d['name'], d['expression']))
        return data_structres_cst


class FunctionGenerator(BaseCST):

    def make_cst(self, data: List[dict]) -> cst.FunctionDef:
        functions_cst = []
        for f_data in data:
            if f_data.get('definition'):
                f_cst = self.create_function_CST(
                    f_data['definition'].get('name'),
                    f_data['definition'].get('decorators'),
                    f_data['definition'].get('arguments'),
                    f_data['definition'].get('statements'),
                    f_data['definition'].get('return_type')
                )
            else:
                f_cst = self.get_node_from_git(
                    f_data['github'].get('url'),
                    f_data['github'].get('filename'),
                    f_data['github'].get('target'),
                    False
                )
            if f_cst:
                functions_cst.append(f_cst)
        return functions_cst


def _make_classes_CST(data: List[dict]) -> List[cst.ClassDef]:
    classes_cst = []
    for cls_d in data:
        if cls_d:
            class_gen = ClassGenerator(cls_d)
            classes_cst.append(class_gen.make_cst())
    return classes_cst


def _make_module(module_body: list) -> cst.Module:
    return cst.Module(
        body=module_body,
        header=base_cst.default_header(),
        footer=[],
        encoding='utf-8',
        default_indent='    ',
        default_newline='\n',
        has_trailing_newline=True
    )


def _generate_code(module: cst.Module, dest_path: Path) -> None:
    raw_code = cst.Module([]).code_for_node(module)
    code_formatter = CodeFormatter(PythonVersion.PY_38, Path().resolve())
    code = code_formatter.format_code(raw_code)
    with open(dest_path, 'w') as file:
        file.write(code)
    return code


def main(data: dict, dest_path: Path) -> str:
    """
    :dest_path - this is a path that the generated *.py file should be saved.
    :data - this is a dictionary that has the class components
    for example,
    {
        "ex1.py": {
            "classes": [{
                "name": "test",
                "description": "This is a test class.",
                "base_classes": ["ABC"],
                "attributes": [
                    {
                        "name": "a",
                        "type": "int",
                        "value": "3"
                    },
                    {
                        "name": "b",
                        "type": "str",
                        "value": "4"
                    },
                    {
                        "name": "c",
                        "type": "bool",
                        "value": "True"
                    }
                ],
                "instance_attributes": [{
                    "name": "test",
                    "value": "None",
                    "type": "str"
                }],
                "instance_methods": [{
                    "github": {
                        "url": "",
                        "filename": "",
                        "target": ""
                    },
                    "definition": {
                        "decorators": ["staticmethod"],
                        "name": "abc",
                        "arguments": [
                            {
                                "name": "a",
                                "type": "int",
                                "value": "1"
                            },
                            {
                                "name": "b",
                                "type": "str",
                                "value": "None"
                            }
                        ],
                        "statements": ["a = b", "return a"],
                        "return_type": "str"
                    }
                }]
            }],
            "functions": [{
                "github": {
                    "url": "",
                    "filename": "",
                    "target": ""
                },
                "definition": {
                    "decorators": ["my_decorator"],
                    "name": "abc",
                    "arguments": [
                        {
                            "name": "a",
                            "type": "int",
                            "value": "1"
                        },
                        {
                            "name": "b",
                            "type": "str",
                            "value": "None"
                        }
                    ],
                    "statements": ["a = b", "return a"],
                    "return_type": "str"
                }
            }],
            "imports": ["impor my_decorator", "from datetime import datetime"],
            "data_structures": [{"name": 'a', "expression": 99}, {"name": "b", "expression": [9, "hello", ["list2", 14, {}]]}]
        },
        "ex2.py": {
            "classes": [],
            "functions": [],
            "imports": [],
            "data_structures": []
        },
    }
    """
    is_valid, err_msg = validation(data)
    if not is_valid:
        raise Exception(err_msg)
    if not os.path.exists(dest_path):
        raise Exception('The dest_path you provide does not exist.')

    import_gen = StatementGenerator()
    data_structure_gen = DataStructureGenerator()
    func_gen = FunctionGenerator()

    for filename, filedata in data.items():
        dest_path = os.path.join(dest_path, filename)
        if not filename.lower().endswith('.py'):
            dest_path = dest_path.rglob("*.py")

        imports_cst: List[cst.SimpleStatementLine] = import_gen.make_cst(filedata['imports'])
        data_structures_cst: List[cst.SimpleStatementLine] = data_structure_gen.make_cst(filedata['data_structures'])
        functions_cst: List[cst.FunctionDef] = func_gen.make_cst(filedata['functions'])
        classes_cst: List[cst.ClassDef] = _make_classes_CST(filedata['classes'])

        module_body = imports_cst + data_structures_cst + classes_cst + functions_cst

        module = _make_module(module_body)
        code = _generate_code(module, dest_path)
        return code
