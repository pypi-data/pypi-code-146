class ErrorParser:
    """
    Abstract class interface for an error parser which parses various standard errors from the backend and returns a
    human readable message.
    """

    def parse(self, api_response):
        """
        This function should either return the human readable message or None if the api_response did
        not return an error message for the parser in question. You can check what endpoint is hit via
        `api_response.api_request.url`
        """
        raise NotImplementedError
