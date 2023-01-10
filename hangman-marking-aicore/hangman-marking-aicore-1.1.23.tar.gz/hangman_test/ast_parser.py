import _ast


def get_variables_and_values(node):
    '''
    Gets the variables and values from the AST.

    Returns
    -------
    variables_dict: dict
        Dictionary with the variables and values.
        The variables are the keys and the corresponding
        values are represented as AST nodes.
    '''
    variables_dict = {}
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables_dict.update(get_variables_and_values(subnode))
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables_dict[name.id] = node.value
    return variables_dict


def get_imports(node):
    imports = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            imports |= get_imports(subnode)
    elif isinstance(node, _ast.Import):
        for name in node.names:
            imports.add(name.name)
    return imports


def get_calls(node):
    calls = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            calls |= get_calls(subnode)
    elif isinstance(node, _ast.Expr):
        if isinstance(node.value, _ast.Call):
            try:
                calls.add(node.value.func.id)
            except AttributeError:
                pass
    return calls


def clean_var_dict(var_dict: dict):
    '''
    Gets a dictionary extracted from the AST and cleans it up.
    '''
    var_dict_test = {}
    for key, value in var_dict.items():

        if isinstance(value, _ast.Call):
            if isinstance(value.func, _ast.Name):
                var_dict_test[key] = value.func.id
            elif isinstance(value.func, _ast.Attribute):
                var_dict_test[key] = value.func.attr

        elif isinstance(value, _ast.List):
            var_dict_test[key] = len(value.elts)


    return var_dict_test
    