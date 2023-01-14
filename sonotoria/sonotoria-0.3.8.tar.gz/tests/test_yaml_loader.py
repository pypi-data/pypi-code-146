from sonotoria import jaml
from sonotoria.jaml import MappedObject

def get_test_file(name):
    return f'tests/yaml_loading_test_files/{name}.yml'

def test_read_simple_yaml():
    # Given
    yaml_file = get_test_file('simple_yaml')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'}
            ]
        }
    }

def test_read_simple_json():
    # Given
    json_file = get_test_file('simple_json')

    # When
    data = jaml.load(json_file)

    # Then
    assert data == {
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'}
            ]
        }
    }

def test_read_yaml_with_reused_variable():
    # Given
    yaml_file = get_test_file('one_var_yaml')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'my_var': 'test',
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'},
                'this is a test'
            ]
        }
    }

def test_read_yaml_with_two_variables():
    # Given
    yaml_file = get_test_file('two_var_yaml')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'my_var': 'test',
        'my_other_var': 'super test',
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'},
                'this is a test',
                'this is a super test'
            ]
        }
    }

def test_read_yaml_with_variable_variable():
    # Given
    yaml_file = get_test_file('var_var_yaml')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'my_var': 'test',
        'my_other_var': 'super test',
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'},
                'this is a test',
                'this is a super test'
            ]
        }
    }

def test_read_yaml_with_variable_in_map():
    # Given
    yaml_file = get_test_file('map_var_yaml')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'my_var': {
            'test': 'plop'
        },
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'},
                'this is a plop'
            ]
        }
    }

def test_read_yaml_with_raw_part():
    # Given
    yaml_file = get_test_file('raw_in_yaml')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'my_var': {
            'test': '{{'
        },
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'},
                'this is a {{'
            ]
        }
    }

def test_read_yaml_with_filter():
    # Given
    yaml_file = get_test_file('filter_in_yaml')
    filters = { 'doublereversed': lambda v: f'{v}{v[::-1]}' }

    # When
    data = jaml.load(yaml_file, filters = filters)

    # Then
    assert data == {
        'my_var': {
            'test': 'plop'
        },
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'},
                'this is a ploppolp'
            ]
        }
    }

def test_read_yaml_with_test():
    # Given
    yaml_file = get_test_file('test_in_yaml')
    tests = { 'http': lambda v: v.startswith('http://') }

    # When
    data = jaml.load(yaml_file, tests = tests)

    # Then
    assert data == {
        'my_var': {
            'test': 'http://plop',
            'test2': 'https://plop'
        },
        'res': {
            'test': True,
            'test2': False
        },
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'}
            ]
        }
    }

def test_read_yaml_with_type():
    # Given
    yaml_file = get_test_file('type_in_yaml')
    class User: # pylint: disable=no-member,too-few-public-methods
        @property
        def name(self):
            return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
    types = { 'user': User }

    # When
    data = jaml.load(yaml_file, types = types)

    # Then
    assert data['res'].first_name == 'eric'
    assert data['res'].last_name == 'final'
    assert data['res'].name == 'Eric Final'

def test_read_yaml_with_map_var():
    # Given
    yaml_file = get_test_file('map_as_var')

    # When
    data = jaml.load(yaml_file)

    # Then
    assert data == {
        'my_var': {
            'test': 'http://plop',
            'test2': 'https://plop'
        },
        'res': {
            'test': 'http://plop',
            'test2': 'https://plop'
        },
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'}
            ]
        }
    }

def test_read_yaml_with_filtered_map_var():
    # Given
    yaml_file = get_test_file('filtered_map_as_var')
    filters = { 'add_plop_to_values': lambda d: { k: f'{v}_lol' for k, v in d.items() } }

    # When
    data = jaml.load(yaml_file, filters = filters)

    # Then
    assert data == {
        'my_var': {
            'test': 'http://plop',
            'test2': 'https://plop'
        },
        'res': {
            'test': 'http://plop_lol',
            'test2': 'https://plop_lol'
        },
        'this': {
            'is': [
                'a',
                'simple',
                {'yaml': 'file'}
            ]
        }
    }

def test_read_yaml_with_var_from_custom_type():
    # Given
    yaml_file = get_test_file('var_from_custom_type')
    class Figure: # pylint: disable=no-member,too-few-public-methods
        pass
    types = {'figure': Figure}

    # When
    figure = jaml.load(yaml_file, types = types)

    # Then
    assert figure.model == 'Goku'
    assert figure.size == '4cm'
    assert figure.material == 'plastic'
    assert figure.serial_number == 'F4521ATB'
    assert figure.price == '45€'
    assert figure.test == 'Goku'

def test_read_yaml_with_context():
    # Given
    context = { 'myvar': 'myval' }
    yaml_file = get_test_file('use_context')

    # When
    figure = jaml.load(yaml_file, context = context)

    # Then
    assert figure['test'] == 'myval'

def test_jaml_load_object_with_construct():
    # Given
    yaml_file = get_test_file('object_with_construct')
    class MyTest(MappedObject): #pylint: disable=too-few-public-methods
        def __init__(self, data):
            self.data = data

    # When
    my_object = jaml.load(yaml_file, types = {'MyTest': MyTest})

    # Then
    assert my_object.data == {'a': 1, 'b': {'c': {'d': 3}}}
