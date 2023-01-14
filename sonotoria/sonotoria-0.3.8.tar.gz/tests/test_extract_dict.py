import sonotoria

from .test_extract_variable import load_test_file


def test_extract_dict():
    # Given
    template = load_test_file('test_extract_dict_template.txt')
    input_ = load_test_file('test_extract_dict_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['parameters'] == {
        'Plop': 'lol',
        'foo': 'bar',
        'PI': 3.14,
        'true': True
    }

def test_extract_dict_template_multiline():
    # Given
    template = load_test_file('test_extract_dict_multiline_template.txt')
    input_ = load_test_file('test_extract_dict_multiline_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['parameters'] == {
        'Plop': 'lol',
        'foo': 'bar',
        'PI': 3.14,
        'true': True
    }

def test_extract_two_dicts():
    # Given
    template = load_test_file('test_extract_two_dicts_template.txt')
    input_ = load_test_file('test_extract_two_dicts_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['parameters'] == {
        'Plop': 'lol',
        'foo': 'bar',
        'PI': 3.14,
        'true': True
    }
    assert data['parameters2'] == {
        'Plop': 'lol',
        'foo': 'bar',
        'PI': 3.14,
        'true': True
    }
