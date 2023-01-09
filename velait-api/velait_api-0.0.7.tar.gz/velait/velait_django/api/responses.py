from rest_framework.response import Response


class APIResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        errors=None,
    ):
        if errors is not None:
            if any((error.get('Name') is None or error.get('Description') is None) for error in errors):
                raise ValueError("Errors do not have 'Name' or 'Description' attribute")

            data = {"Errors": errors}
        else:
            data = {"Results": data}

        super(APIResponse, self).__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
