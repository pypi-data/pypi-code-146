import sonotoria

from .test_extract_variable import load_test_file


def test_extract_list():
    # Given
    template = load_test_file('test_extract_list_template.txt')
    input_ = load_test_file('test_extract_list_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['parameters'] == [
        'lol',
        'bar',
        3.14,
        True
    ]


def test_extract_list_template_multiline():
    # Given
    template = load_test_file('test_extract_list_multiline_template.txt')
    input_ = load_test_file('test_extract_list_multiline_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['parameters'] == [
        'lol',
        'bar',
        3.14,
        True
    ]
