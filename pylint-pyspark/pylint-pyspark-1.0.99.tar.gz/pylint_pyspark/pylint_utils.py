##
# Copyright 2020 Palantir Technologies, Inc. All rights reserved.
# Licensed under the MIT License (the "License"); you may obtain a copy of the
# license at https://github.com/palantir/pyspark-style-guide/blob/develop/LICENSE
##

import astroid


def compute_arguments_length(arguments):
    args_length = 0
    for arg in arguments:
        args_length += get_length(arg)
    return args_length


def compute_target_lengths(targets):
    total_length = 0
    for target in targets:
        total_length += get_length(target)
    return total_length


def select_contains_alias_call(expression):
    if not hasattr(expression.value, "func") or not hasattr(
        expression.value.func, "attrname"
    ):
        return False
    if expression.value.func.attrname == "select":
        for arg in expression.value.args:
            if isinstance(arg, astroid.nodes.Call):
                if arg.func.attrname == "alias":
                    return True
    return False


def select_contains_cast_call(expression):
    if not hasattr(expression.value, "func") or not hasattr(
        expression.value.func, "attrname"
    ):
        return False
    if expression.value.func.attrname == "select":
        for arg in expression.value.args:
            if isinstance(arg, astroid.nodes.Call):
                if arg.func.attrname == "cast":
                    return True
    return False


def module_contains_display(expression):
    try:
        contains_func_attribute = hasattr(expression.value, "func")
    except AttributeError:
        contains_func_attribute = False
    try:
        contains_attrname = hasattr(expression.value.func, "attrname")
    except AttributeError:
        contains_attrname = False
    try:
        contains_display_attr = expression.value.func.attrname == "display"
    except AttributeError:
        contains_display_attr = False
    contains_display_func = False
    for arg in expression.value.args:
        contains_display_func = (
            isinstance(arg.parent, astroid.nodes.Call)
            and hasattr(arg.parent.func, "name")
            and arg.parent.func.name == "display"
        )
    return (
        contains_func_attribute and contains_attrname and contains_display_attr
    ) or (contains_func_attribute and contains_display_func)


def module_contains_show(expression):
    try:
        contains_func_attribute = hasattr(expression.value, "func")
    except AttributeError:
        contains_func_attribute = False
    try:
        contains_attrname = hasattr(expression.value.func, "attrname")
    except AttributeError:
        contains_attrname = False
    try:
        contains_show_attr = expression.value.func.attrname == "show"
    except AttributeError:
        contains_show_attr = False
    contains_show_func = False
    for arg in expression.value.args:
        contains_show_func = (
            isinstance(arg.parent, astroid.nodes.Call)
            and hasattr(arg.parent.func, "name")
            and arg.parent.func.name == "show"
        )
    return (contains_func_attribute and contains_attrname and contains_show_attr) or (
        contains_func_attribute and contains_show_func
    )


def module_contains_print(expression):
    contains_func_attribute = hasattr(expression.value, "func")
    contains_print_func = False
    for arg in expression.value.args:
        contains_print_func = (
            isinstance(arg.parent, astroid.nodes.Call)
            and hasattr(arg.parent.func, "name")
            and arg.parent.func.name == "print"
        )
    return contains_func_attribute and contains_print_func


def is_line_split(val):
    line = val.lineno
    if isinstance(val, astroid.nodes.FunctionDef):
        for arg in val.args.args:
            if arg.lineno != line:
                return True
        return False
    if isinstance(val, astroid.nodes.Call):
        for arg in val.args:
            if arg.lineno != line:
                return True
        return False
    if isinstance(val, astroid.nodes.Assign):
        if hasattr(val.value, "args"):
            for arg in val.value.args:
                if arg.lineno != line:
                    return True
        if hasattr(val.value, "elts"):
            for arg in val.value.elts:
                if arg.lineno != line:
                    return True
        return False


def get_binary_op_complexity(arg):
    if isinstance(arg, astroid.nodes.BinOp):
        nested_complexity = get_binary_op_complexity(
            arg.left
        ) + get_binary_op_complexity(arg.right)
        # We need this Because essentially multiple ops are nested
        return 1 + (nested_complexity if nested_complexity > 0 else 1)
    return 0


def get_length(arg):
    if isinstance(arg, astroid.nodes.Const):
        length = len(str(arg.value))
        if isinstance(arg.pytype(), str):
            length += 2  # Quotes
        return length
    if isinstance(arg, astroid.nodes.BinOp):
        base_length = 3  # _+_
        compound_length = get_length(arg.left) + get_length(arg.right)
        # print "Binop length %d" % (compound_length)
        return base_length + compound_length
    if isinstance(arg, astroid.nodes.Call):
        # print arg
        base_length = 2  # Open and closing brackets
        length = get_length(arg.func) + compute_arguments_length(arg.args) + base_length
        # print "Call length %s" % length
        return length
    if isinstance(arg, astroid.nodes.Attribute):
        base_length = 1  # Period
        if hasattr(arg.expr, "name"):
            expr_length = len(arg.expr.name)
        else:
            expr_length = get_length(arg.expr)
        total_length = expr_length + base_length + len(arg.attrname)
        return total_length
    if isinstance(arg, astroid.nodes.Assign):
        # print arg
        base_length = 2  # Brackets
        target_length = compute_target_lengths(arg.targets)
        value_length = get_length(arg.value)
        return base_length + value_length + target_length
    if isinstance(arg, astroid.nodes.Tuple):
        args_length = 0
        for value in arg.elts:
            args_length += len(value.name)
        if len(arg.elts) > 1:
            args_length += (len(arg.elts) - 1) * 2
        return args_length
    if isinstance(arg, astroid.nodes.Name):
        return len(arg.name)
    if isinstance(arg, astroid.nodes.AssignName):
        return len(arg.name)
    if isinstance(arg, astroid.nodes.Compare):
        total_length = 0
        for op in arg.ops:
            total_length += 2 + len(op[0]) + get_length(op[1])
        total_length += get_length(arg.left)
        return total_length
    if isinstance(arg, astroid.nodes.List):
        total_length = 0
        for value in arg.elts:
            total_length += get_length(value)
        return total_length
    if isinstance(arg, astroid.nodes.Subscript):
        base_length = 2  # brackets
        total_length = base_length + get_length(arg.value) + get_length(arg.slice)
        return total_length
    if isinstance(arg, astroid.nodes.JoinedStr):
        base_length = 3  # quotes and 'f'
        total_length = 0
        for value in arg.values:
            total_length += get_length(value)
        total_length += base_length
        return total_length
    if isinstance(arg, astroid.nodes.FormattedValue):
        base_length = 3  # quotes and 'f'
        total_length = 0
        total_length += base_length + get_length(arg.value)
        return total_length
    if isinstance(arg, astroid.nodes.Starred):
        base_length = 1  # '*'
        total_length = get_length(arg.value)
        total_length += base_length
        return total_length
    if isinstance(arg, astroid.nodes.Slice):
        total_length = 0
        number_of_colon = 0
        try:
            lower_length = get_length(arg.lower)
        except TypeError:
            lower_length = 0
        try:
            step_length = get_length(arg.step)

        except TypeError:
            step_length = 0
        try:
            upper_length = get_length(arg.upper)
        except TypeError:
            upper_length = 0
        if lower_length >= 1 or upper_length >= 1:
            number_of_colon += 1
        # step should always have two
        if step_length >= 1:
            number_of_colon = 2
        total_length += lower_length + step_length + upper_length + number_of_colon
        return total_length
    if isinstance(arg, astroid.nodes.UnaryOp):
        base_length = 1  # operator
        total_length = len(arg.operand)
        total_length += base_length
        return total_length
    if arg is None:
        return 0
    print(f"Unhandled {arg}")
    return 0
