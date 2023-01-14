import sonotoria

from .test_extract_variable import load_test_file


def test_extract_cond():
    # Given
    template = load_test_file('test_extract_cond_template.txt')
    input_ = load_test_file('test_extract_cond_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['test'] is True
    assert data['test2'] is False
    assert data['bruh'] == 'val1'
    assert data['bruh2'] is None


def test_extract_rest():
    # Given
    template = load_test_file('test_rest_template.txt')
    input_ = load_test_file('test_rest_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['params']['test'] == 'Looks like a test variable, huh'
    assert data['params']['lol'] == 'This might be a fun variable'
    assert data['params']['plop'] == 'Plop might just be the next best variable name'
    assert data['return'] == 'Pretty much nothing, sadly'
    assert data['rtype'] is None
    assert data['return_given'] is True
    assert data['rtype_given'] is False
