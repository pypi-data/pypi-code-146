def test_test_working():
    # Given
    hello = 'world'

    # When
    res = 'hello' + ' ' +  hello

    # Then
    assert res == 'hello world'
