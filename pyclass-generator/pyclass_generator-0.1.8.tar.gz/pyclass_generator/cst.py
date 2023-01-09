from abc import ABC
from pathlib import Path
from typing import Any, List, Optional  # Tuple, Dict

import git
import libcst as cst

from .utils import logger

# import libcst.matchers as m


class VisitorCollector(cst.CSTVisitor):
    def __init__(self, target_name: str = None, is_method: bool = False):
        self.target_name: str = target_name
        self.is_method: bool = is_method
        self.target_node: cst.FunctionDef = None

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        return self.is_method

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        if node.name.value == self.target_name:
            self.target_node = node
        return False


# class TransformerCollector(cst.CSTTransformer):
#     def __init__(self, *args, **kwargs):
#         pass

#     def leave_ClassDef(
#         self, original_node: cst.ClassDef, updated_node: cst.ClassDef
#     ) -> cst.CSTNode:
#         if m.matches(updated_node.name, m.Name()):
#             return updated_node.with_changes(
#                 name=cst.Name(
#                     self.class_name
#                 )
#             )
#         return updated_node

#     def leave_FunctionDef(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         log_stmt = cst.Expr(cst.parse_expression("print('returning')"))
#         return cst.FlattenSentinel([log_stmt, cst.Expr(cst.Newline()), updated_node])

#     def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
#         if m.matches(original_node.func, m.Name()):
#             return original_node.with_changes(
#                 func=cst.Name(
#                     "renamed_" + cst.ensure_type(original_node.func, cst.Name).value
#                 )
#             )
#         return original_node

#     def leave_Assign(self, old_node, updated_node):
#         log_stmt = cst.Expr(cst.parse_expression("print('returning')"))
#         return cst.FlattenSentinel([log_stmt, cst.Expr(cst.Newline()), updated_node])

#     def leave_AnnAssign(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         return updated_node

#     def leave_AsName(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         return updated_node

#     def leave_AugAssign(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         return updated_node

#     def leave_Decorator(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         return updated_node

#     def leave_SimpleStatementLine(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         if m.matches(original_node.body[0], m.Pass()):
#             attr_body = []
#             for f in self.fields:
#                 attr_body.append(cst.Expr(cst.parse_module(f)))
#             return original_node.with_changes(
#                 body=[
#                     attr_body
#                 ]
#             )
#         return original_node

#     def leave_SimpleStatementSuite(
#         self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
#     ) -> cst.CSTNode:
#         return updated_node


class GitRemoteProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        logger.info('update(%s, %s, %s, %s)' % (op_code, cur_count, max_count, message))


class BaseCST(ABC):

    def git_clone_to_temp(self, url: str) -> None:
        try:
            git.Repo.clone_from(url, './temp', progress=GitRemoteProgress())
        except git.GitCommandError as e:
            logger.info(str(e))
        except Exception as e:
            raise Exception(e)
        return

    def get_node_from_git(
        self, gitrepo_url: str, filename: str, target: str, is_method: bool = False
    ) -> cst.FunctionDef:
        self.git_clone_to_temp(gitrepo_url)
        target_file = Path(f'./temp/{filename}')
        if target_file.is_file():
            with open(f'./temp/{filename}') as f:
                source = f.read()
            source_tree = cst.parse_module(source)
            visitor = VisitorCollector(target, is_method)
            source_tree.visit(visitor)
            return visitor.target_node
        else:
            raise Exception(f'The file {filename} does not exist in the git repository.')

    def split_statement(
            self, statement: str, word: str, left: bool = False, right: bool = False) -> list:
        try:
            if left:
                return (statement.split(word, 2)[0]).strip()
            elif right:
                return (statement.split(word, 2)[1]).strip()
            else:
                return statement.split(word, 2)
        except Exception:
            raise Exception('Invailid Statement')

    def default_leading_lines(self) -> List[cst.EmptyLine]:
        return [cst.EmptyLine(
                indent=False, whitespace=cst.SimpleWhitespace(value='',),
                comment=None, newline=cst.Newline(value=None,),)]

    def default_comma(self) -> cst.Comma:
        return cst.Comma(
            whitespace_before=cst.SimpleWhitespace(value='',),
            whitespace_after=cst.SimpleWhitespace(value=' ',)
        )

    def default_equal(self) -> cst.AssignEqual:
        return cst.AssignEqual(
            whitespace_after=cst.SimpleWhitespace(value=' ',),
            whitespace_before=cst.SimpleWhitespace(value=' ',)
        )

    def default_header(self) -> List[cst.EmptyLine]:
        return [
            cst.EmptyLine(
                indent=True,
                whitespace=cst.SimpleWhitespace(value='',),
                comment=None,
                newline=cst.Newline(value=None,)
            )
        ]

    def create_target_CST(self, name: str) -> cst.AssignTarget:
        return cst.AssignTarget(target=cst.Name(value=name))

    def create_class_attr_CST(self, name: str, value: str, val_type: str = None) -> cst.SimpleStatementLine:
        attr_name = cst.Name(name)

        if val_type == 'dict':
            attr_value = cst.Dict(value)
        elif val_type == 'list':
            attr_value = cst.List(value)
        elif val_type == 'tuple':
            attr_value = cst.Tuple(value)
        elif val_type == 'float':
            attr_value = cst.Float(value)
        elif val_type == 'bool':
            attr_value = cst.Name(value)
        elif val_type == 'int' or (val_type == 'int' and value.isnumeric()):
            attr_value = cst.Integer(value)
        else:
            attr_value = cst.SimpleString(f"'{value}'")
        if val_type:
            annotation = cst.Annotation(
                annotation=cst.Name(val_type), whitespace_before_indicator=cst.SimpleWhitespace(value=''))
            return cst.SimpleStatementLine(
                body=[
                    cst.AnnAssign(
                        target=attr_name,
                        annotation=annotation,
                        value=attr_value,
                        equal=cst.AssignEqual(
                            whitespace_before=cst.SimpleWhitespace(value=' ',),
                            whitespace_after=cst.SimpleWhitespace(value=' ',)
                        )
                    )
                ],
                leading_lines=self.default_leading_lines()
            )
        else:
            return cst.SimpleStatementLine(
                body=[
                    cst.Assign(
                        targets=(
                            cst.AssignTarget(
                                target=attr_name
                            )
                        ),
                        value=attr_value,
                        equal=cst.AssignEqual(
                            whitespace_before=cst.SimpleWhitespace(value=' ',),
                            whitespace_after=cst.SimpleWhitespace(value=' ',)
                        )
                    )
                ],
                leading_lines=self.default_leading_lines()
            )

    def create_instance_attr_CST(self, name: str, value: str) -> cst.SimpleStatementLine:
        targets = [
            cst.AssignTarget(
                target=cst.Attribute(
                    value=cst.Name('self'),
                    attr=cst.Name(name)
                )
            )
        ]
        value = cst.Name(value)
        return cst.SimpleStatementLine(body=[cst.Assign(targets=targets, value=value)])

    def create_getter_CST(self, name: str, return_type: str) -> cst.FunctionDef:
        getter_name: cst.Name = cst.Name(name)
        params: cst.Parameters = cst.Parameters(
            params=[
                cst.Param(cst.Name('self'), star=''),
                cst.Param(cst.Name(name), cst.Annotation(cst.Name(return_type)))
            ]
        )
        body: cst.IndentedBlock = cst.IndentedBlock(
            body=[
                cst.SimpleStatementLine(body=[
                    cst.Return(
                        value=cst.Attribute(
                            value=cst.Name('self'),
                            attr=cst.Name('_' + name)
                        )
                    )
                ])
            ]
        )
        decorators: List[cst.Decorator] = [
            cst.Decorator(
                decorator=cst.Name('property')
            )
        ]
        returns: cst.Annotation = cst.Annotation(
            annotation=cst.Name(return_type),
            whitespace_before_indicator=cst.SimpleWhitespace(value=' ',)
        )
        return cst.FunctionDef(
            name=getter_name, params=params, body=body, decorators=decorators,
            returns=returns, leading_lines=self.default_leading_lines()
        )

    def create_setter_CST(self, name: str, return_type: str) -> cst.FunctionDef:
        setter_name: cst.Name = cst.Name(name)
        params: cst.Parameters = cst.Parameters(
            params=[
                cst.Param(cst.Name('self'), star='', comma=self.default_comma()),
                cst.Param(cst.Name(name), cst.Annotation(
                    cst.Name(return_type),
                    whitespace_before_indicator=cst.SimpleWhitespace(value=' ',)), star=''
                )
            ]
        )
        body: cst.IndentedBlock = cst.IndentedBlock(
            body=[
                cst.SimpleStatementLine(
                    body=[
                        cst.Assign(
                            targets=[
                                cst.AssignTarget(
                                    cst.Attribute(
                                        value=cst.Name('self'),
                                        attr=cst.Name('_' + name)
                                    )
                                )
                            ],
                            value=cst.Name(name)
                        )
                    ]
                )
            ]
        )
        decorators: List[cst.Decorator] = [
            cst.Decorator(cst.Attribute(value=cst.Name(name), attr=cst.Name('setter')))
        ]
        returns: cst.Annotation = cst.Annotation(
            annotation=cst.Name(return_type),
            whitespace_before_indicator=cst.SimpleWhitespace(value=' ',)
        )
        return cst.FunctionDef(
            name=setter_name, params=params, body=body, decorators=decorators,
            returns=returns, leading_lines=self.default_leading_lines()
        )

    def create_instance_method_CST(
        self,
        name: str,
        decorators: List[str],
        arguments: List[dict],
        statements: List[str],
        return_type: str
    ) -> cst.FunctionDef:
        method_name: cst.Name = cst.Name(name)
        if 'staticmethod' in decorators:
            params: List[cst.Param] = []
        elif classmethod in decorators:
            params: List[cst.Param] = [
                cst.Param(cst.Name('cls'), comma=self.default_comma(), star='')
            ]
        else:
            params: List[cst.Param] = [
                cst.Param(cst.Name('self'), comma=self.default_comma(), star='')
            ]
        for arg in arguments:
            if arg.get('type') == 'dict':
                default_value = cst.Dict(arg.get('value'))
            elif arg.get('type') == 'list':
                default_value = cst.List(arg.get('value'))
            elif arg.get('type') == 'tuple':
                default_value = cst.Tuple(arg.get('value'))
            elif arg.get('type') == 'float':
                default_value = cst.Float(str(arg.get('value')))
            elif arg.get('type') == 'int':
                default_value = cst.Integer(str(arg.get('value')))
            else:  # case of ['bool', 'str']
                default_value = cst.Name(str(arg.get('value')))
            params.append(
                cst.Param(
                    name=cst.Name(arg.get('name')),
                    annotation=cst.Annotation(
                        annotation=cst.Name(arg.get('type')),
                        whitespace_before_indicator=cst.SimpleWhitespace(value='',)
                    ),
                    default=default_value,
                    star='',
                    comma=self.default_comma(),
                    equal=self.default_equal()
                )
            )
        body: List[cst.SimpleStatementLine] = []
        for statement in statements:
            if '=' in statement:
                statement_name = self.split_statement(statement=statement, word='=', left=True)
                statement_value = self.split_statement(statement=statement, word='=', right=True)
                body.append(cst.SimpleStatementLine(body=[
                    cst.Assign(
                        targets=[cst.AssignTarget(cst.Name(statement_name))],
                        value=cst.Name(statement_value)
                    )
                ]))
            elif 'return' in statement:
                statement_value = self.split_statement(
                    statement=statement, word='return', right=True)
                body.append(cst.SimpleStatementLine(body=[
                    cst.Return(
                        value=cst.Name(statement_value),
                        whitespace_after_return=cst.SimpleWhitespace(value=' ')
                    )
                ]))
        decorators_CST: List[cst.Decorator] = []
        for decorator in decorators:
            decorators_CST.append(cst.Decorator(decorator=cst.Name(decorator)))
        returns: cst.Annotation = cst.Annotation(
            annotation=cst.Name(return_type),
            whitespace_before_indicator=cst.SimpleWhitespace(value=' ',),
            whitespace_after_indicator=cst.SimpleWhitespace(value=' ',)
        )
        return cst.FunctionDef(
            name=method_name,
            params=cst.Parameters(params=params),
            body=cst.IndentedBlock(body=body),
            decorators=decorators_CST,
            returns=returns,
            leading_lines=self.default_leading_lines()
        )

    def create_import_CST(self, statement: str = None) -> cst.SimpleStatementLine:
        return cst.parse_statement(statement)

    def create_data_structure_CST(self, name: str, value: Any) -> cst.SimpleStatementLine:
        expression = cst.parse_expression(str(value))
        target = self.create_target_CST(name)
        return cst.SimpleStatementLine(
            body=[
                cst.Assign(
                    targets=[target],
                    value=expression
                )
            ]
        )

    def create_function_CST(
        self,
        name: str,
        decorators: List[str],
        arguments: List[dict],
        statements: List[str],
        return_type: str
    ) -> cst.FunctionDef:
        method_name: cst.Name = cst.Name(name)
        params: List[cst.Param] = []

        for arg in arguments:
            if arg.get('type') == 'dict':
                default_value = cst.Dict(arg.get('value'))
            elif arg.get('type') == 'list':
                default_value = cst.List(arg.get('value'))
            elif arg.get('type') == 'tuple':
                default_value = cst.Tuple(arg.get('value'))
            elif arg.get('type') == 'float':
                default_value = cst.Float(str(arg.get('value')))
            elif arg.get('type') == 'int':
                default_value = cst.Integer(str(arg.get('value')))
            else:  # case of ['bool', 'str']
                default_value = cst.Name(str(arg.get('value')))
            params.append(
                cst.Param(
                    name=cst.Name(arg.get('name')),
                    annotation=cst.Annotation(
                        annotation=cst.Name(arg.get('type')),
                        whitespace_before_indicator=cst.SimpleWhitespace(value='',)
                    ),
                    default=default_value,
                    star='',
                    comma=self.default_comma(),
                    equal=self.default_equal()
                )
            )
        body: List[cst.SimpleStatementLine] = []
        for statement in statements:
            body.append(cst.parse_statement(statement))
        decorators_CST: List[cst.Decorator] = []
        for decorator in decorators:
            decorators_CST.append(cst.Decorator(decorator=cst.Name(decorator)))
        returns: cst.Annotation = cst.Annotation(
            annotation=cst.Name(return_type),
            whitespace_before_indicator=cst.SimpleWhitespace(value=' ',),
            whitespace_after_indicator=cst.SimpleWhitespace(value=' ',)
        )
        return cst.FunctionDef(
            name=method_name,
            params=cst.Parameters(params=params),
            body=cst.IndentedBlock(body=body),
            decorators=decorators_CST,
            returns=returns,
            leading_lines=self.default_leading_lines()
        )
