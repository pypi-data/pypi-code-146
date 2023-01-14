import sonotoria

def load_test_file(file):
    with open(f'tests/test_files/{file}', 'r', encoding='utf-8') as fdesc:
        return fdesc.read()

def test_extract_single_variable():
    # Given
    template = load_test_file('test_extract_single_variable_template.txt')
    input_ = load_test_file('test_extract_single_variable_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['tailor_name'] == 'Henry'

def test_extract_single_variable_with_space():
    # Given
    template = load_test_file('test_extract_single_variable_template.txt')
    input_ = load_test_file('test_extract_single_variable_with_space_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['tailor_name'] == 'John Do'

def test_extract_two_variables():
    # Given
    template = load_test_file('test_extract_two_variables_template.txt')
    input_ = load_test_file('test_extract_two_variables.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['tailor_last_name'] == 'Williams'
    assert data['tailor_first_name'] == 'Henry'

def test_extract_six_variables_multiline_string():
    # Given
    template = load_test_file('test_extract_six_variables_template.txt')
    input_ = load_test_file('test_extract_six_variables_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['father'] == 'Eric'
    assert data['mother'] == 'Nathalie'
    assert data['nb_siblings'] == 3
    assert data['daughter'] == 'Atalza'
    assert data['cat'] == 'Ellana'
    assert data['fan'] == 'Cassius'

def test_extract_six_variables_with_float():
    # Given
    template = load_test_file('test_extract_six_variables_with_float_template.txt')
    input_ = load_test_file('test_extract_six_variables_with_float_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['father'] == 'Rich'
    assert data['mother'] == 'Tired'
    assert data['nb_siblings'] == 2.6
    assert data['daughter'] == 'LaTex'
    assert data['cat'] == 'Féline'
    assert data['fan'] == '3.14'

def test_extract_variables_with_misc_types():
    # Given
    template = load_test_file('test_extract_variables_with_misc_types_template.txt')
    input_ = load_test_file('test_extract_variables_with_misc_types_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['age'] == 12
    assert data['truth'] is False
    assert data['truth2'] is True
    assert data['number'] == 'Pi'
    assert data['value'] == 2.45
    assert data['place'] == 'church'
    assert data['n1'] == 'true'
    assert data['n2'] == '2.1'
    assert data['bruh'] is None
    assert data['bruh1'] is None
    assert data['bruh2'] is None

def test_extract_variables_used_twice():
    # Given
    template = load_test_file('test_extract_variables_used_twice_template.txt')
    input_ = load_test_file('test_extract_variables_used_twice_input.txt')

    # When
    data = sonotoria.extract(template, input_)

    # Then
    assert data['var'] == 'test'
