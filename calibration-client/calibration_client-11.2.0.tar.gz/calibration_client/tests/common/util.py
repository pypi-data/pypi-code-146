"""Test utility functions"""


def debug_response(response):
    print('*' * 100)
    print('response.status_code =>', str(response.status_code))
    print('response.content =>', str(response.content))
    print('*' * 100)

    # Raise Error to show response content
    raise NameError('See response message content')
