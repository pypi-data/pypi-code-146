class UnknownConnector(Exception):
    def __init__(self, name):
        super().__init__(f'Unknown connector name {name}')

class UnsupportedFormat(Exception):
    def __init__(self, fmt):
        super().__init__(f'Unsupported format {fmt}')

class MissingConfiguration(Exception):
    def __init__(self, name):
        super().__init__(f'{name} is required')

class JobError(Exception):
    pass

class HTTPError(Exception):
    def __init__(self, method, response, error_message):
        status_code = response.status_code
        url = response.url
        super().__init__(f'{status_code} code for {method} {url}: {error_message}')

class UnsupportedCloudServiceScheme(Exception):
    def __init__(self, scheme):
        super().__init__(f'The cloud service scheme {scheme} is unsupported')

class UnsupportedCloudService(Exception):
    def __init__(self, service):
        super().__init__(f'The cloud service {service} is unsupported')
