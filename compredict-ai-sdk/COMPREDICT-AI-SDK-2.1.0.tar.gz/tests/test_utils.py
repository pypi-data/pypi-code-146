from compredict.utils.utils import extract_error_message


def test_extract_error_message():
    text = "Exception Value: name 'DataFormatError' is not defined " \
           "Request information:"
    assert extract_error_message(text) == "name 'DataFormatError' is not defined"


def test_extract_error_message_when_key_words_not_found():
    text = 'Some other text with Exception, but without' \
           'right key words'
    assert extract_error_message(text) == "Internal Server Error"
