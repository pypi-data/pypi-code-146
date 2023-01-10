import logging

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('pyclass_generator')


def validation(data: dict) -> tuple:
    err_msg = ''
    is_valid = True
    try:
        for filename, filedata in data.items():
            if not isinstance(filedata['classes'], list) or not isinstance(filedata['functions'], list) \
                or not isinstance(filedata['imports'], list) \
                    or not isinstance(filedata['data_structures'], list):
                is_valid = False
                err_msg = 'The classes or functions or imports or data_structures should be a list'
                break
            for class_data in filedata['classes']:
                if class_data['name']:
                    if not isinstance(class_data['name'], str):
                        is_valid = False
                        err_msg = 'class name should be a str.'
                        break
                    if not isinstance(class_data['description'], str):
                        is_valid = False
                        err_msg = 'class description should be a str.'
                        break
                    if not isinstance(class_data['base_classes'], list):
                        is_valid = False
                        err_msg = 'class base_classes should be a list.'
                        break
                    else:
                        for base_class in class_data['base_classes']:
                            if not isinstance(base_class, str):
                                is_valid = False
                                err_msg = 'class base_class should be a str.'
                                break
                    if not isinstance(class_data['attributes'], list):
                        is_valid = False
                        err_msg = 'class attributes should be a list.'
                        break
                    else:
                        for attr in class_data['attributes']:
                            if not isinstance(attr, dict):
                                is_valid = False
                                err_msg = 'class attribute should be a dict.'
                                break
                            else:
                                if sorted(attr.keys()) != sorted(['name', 'type', 'value']):
                                    is_valid = False
                                    err_msg = 'class attribute should have the name, type and value as the element key'
                                    break
                                else:
                                    for key, val in attr.items():
                                        if not isinstance(val, str):
                                            is_valid = False
                                            err_msg = 'class attribute should have a str as the element value'
                                            break

                    if not isinstance(class_data.get('instance_attributes'), list):
                        is_valid = False
                        err_msg = 'The class instance_attributes should be a list.'
                        break
                    else:
                        for attr in class_data['instance_attributes']:
                            if not isinstance(attr, dict):
                                is_valid = False
                                err_msg = 'class instance_attribute should be a dict.'
                                break
                            else:
                                if sorted(attr.keys()) != sorted(['name', 'type', 'value']):
                                    is_valid = False
                                    err_msg = 'class instance_attribute should have the name, type and value as the element key'
                                    break
                                else:
                                    for key, val in attr.items():
                                        if not isinstance(val, str):
                                            is_valid = False
                                            err_msg = 'class instance_attribute should have a str as the element value'
                                            break

                    if not isinstance(class_data['instance_methods'], list):
                        is_valid = False
                        err_msg = 'The class instance_methods should be a list.'
                        break
                    else:
                        for method in class_data['instance_methods']:
                            if sorted(method.keys()) == sorted(['github', 'definition']):
                                is_valid = False
                                err_msg = f'a Class method could not have both the github and definition as the key: {method}.'
                                break
                            else:
                                if method.get('github'):
                                    if not isinstance(method['github'], dict):
                                        is_valid = False
                                        err_msg = 'class github data should be a dict.'
                                        break
                                    else:
                                        if sorted(method['github'].keys()) == sorted(['url', 'filename', 'target']):
                                            for key, val in method['github'].items():
                                                if not isinstance(val, str):
                                                    is_valid = False
                                                    err_msg = 'class github every element should be a str.'
                                                    break
                                        else:
                                            is_valid = False
                                            err_msg = 'class github should have the url, filename and target as the key'
                                            break
                                elif method.get('definition'):
                                    if not isinstance(method['definition'], dict):
                                        is_valid = False
                                        err_msg = 'class instance method definition should be a dict.'
                                        break
                                    else:
                                        if sorted(method['definition'].keys()) == sorted(['decorators', 'name', 'arguments', 'statements', 'return_type']):
                                            if not isinstance(method['definition']['decorators'], list):
                                                is_valid = False
                                                err_msg = 'class instance method decorators should be a list'
                                                break
                                            else:
                                                for decorator in method['definition']['decorators']:
                                                    if not isinstance(decorator, str):
                                                        is_valid = False
                                                        err_msg = 'class instance method decorator should be a str'
                                                        break
                                            if not isinstance(method['definition']['name'], str):
                                                is_valid = False
                                                err_msg = 'class instance method name should be a str'
                                                break
                                            if not isinstance(method['definition']['arguments'], list):
                                                is_valid = False
                                                err_msg = 'class instance method arguments should be a list'
                                                break
                                            else:
                                                for arg in method['definition']['arguments']:
                                                    if sorted(arg.keys()) != sorted(['name', 'type', 'value']):
                                                        is_valid = False
                                                        err_msg = 'class instance method argument should have the name, type and value as the element key'
                                                        break
                                                    else:
                                                        for key, val in arg.items():
                                                            if not isinstance(val, str):
                                                                is_valid = False
                                                                err_msg = 'class instance method argument should have a str as the dict element.'
                                                                break
                                            if not isinstance(method['definition']['statements'], list):
                                                is_valid = False
                                                err_msg = 'class instance method statements should be a list'
                                                break
                                            else:
                                                for statement in method['definition']['statements']:
                                                    if not isinstance(statement, str):
                                                        is_valid = False
                                                        err_msg = 'class instance method statement should be a str'
                                                        break
                                            if not isinstance(method['definition']['return_type'], str):
                                                is_valid = False
                                                err_msg = 'class instance method return_type should be a str'
                                                break
                                        else:
                                            is_valid = False
                                            err_msg = 'class instance method definition should have the decorators, name, arguments, statements and return_type as the key'
                                            break
                                else:
                                    is_valid = False
                                    err_msg = f'A  Class instance method should have the github or definition as the key: {method}.'
                                    break
            for function_data in filedata['functions']:
                if sorted(function_data.keys()) == sorted(['github', 'definition']):
                    is_valid = False
                    err_msg = f'functions could not have both the github and definition as the key: {function_data}.'
                    break
                else:
                    if function_data.get('github'):
                        if not isinstance(function_data['github'], dict):
                            is_valid = False
                            err_msg = 'function github data should be a dict.'
                            break
                        else:
                            if sorted(function_data['github'].keys()) == sorted(['url', 'filename', 'target']):
                                for key, val in function_data['github'].items():
                                    if not isinstance(val, str):
                                        is_valid = False
                                        err_msg = 'function github every element should be a str.'
                                        break
                            else:
                                is_valid = False
                                err_msg = 'function github should have the url, filename and target as the key'
                                break
                    elif function_data.get('definition'):
                        if not isinstance(function_data['definition'], dict):
                            is_valid = False
                            err_msg = 'function definition should be a dict.'
                            break
                        else:
                            if sorted(function_data['definition'].keys()) == sorted(['decorators', 'name', 'arguments', 'statements', 'return_type']):
                                if not isinstance(function_data['definition']['decorators'], list):
                                    is_valid = False
                                    err_msg = 'function decorators should be a list'
                                    break
                                else:
                                    for decorator in function_data['definition']['decorators']:
                                        if not isinstance(decorator, str):
                                            is_valid = False
                                            err_msg = 'function decorator should be a str'
                                            break
                                if not isinstance(function_data['definition']['name'], str):
                                    is_valid = False
                                    err_msg = 'function name should be a str'
                                    break
                                if not isinstance(function_data['definition']['arguments'], list):
                                    is_valid = False
                                    err_msg = 'function arguments should be a list'
                                    break
                                else:
                                    for arg in function_data['definition']['arguments']:
                                        if sorted(arg.keys()) != sorted(['name', 'type', 'value']):
                                            is_valid = False
                                            err_msg = 'function argument should have the name, type and value as the element key'
                                            break
                                        else:
                                            for key, val in arg.items():
                                                if not isinstance(val, str):
                                                    is_valid = False
                                                    err_msg = 'function argument should have a str as the dict element.'
                                                    break
                                if not isinstance(function_data['definition']['statements'], list):
                                    is_valid = False
                                    err_msg = 'function statements should be a list'
                                    break
                                else:
                                    for statement in function_data['definition']['statements']:
                                        if not isinstance(statement, str):
                                            is_valid = False
                                            err_msg = 'function statement should be a str'
                                            break
                                if not isinstance(function_data['definition']['return_type'], str):
                                    is_valid = False
                                    err_msg = 'function return_type should be a str'
                                    break
                            else:
                                is_valid = False
                                err_msg = 'function definition should have the decorators, name, arguments, statements and return_type as the key'
                                break
                    else:
                        is_valid = False
                        err_msg = f'function should have the github or definition as the key: {function_data}.'
                        break
            for import_statement in filedata['imports']:
                if not isinstance(import_statement, str):
                    is_valid = False
                    err_msg = 'import statement should be a str'
                    break
            for data_structure in filedata['data_structures']:
                if sorted(data_structure.keys()) != sorted(['name', 'expression']):
                    is_valid = False
                    err_msg = 'data_structure should have the name and expression as the key'
                    break

    except Exception as e:
        is_valid = False
        err_msg = str(e)
    return is_valid, err_msg
