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
            data = {"errors": [{'name': error.name, 'description': error.description} for error in errors]}
        elif not (isinstance(data, dict) and data.get('pagination') is not None):
            data = {"results": data}

        super(APIResponse, self).__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
