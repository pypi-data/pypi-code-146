from rest_framework.views import exception_handler

from velait.common.database.exceptions import VelaitError
from velait.velait_django.main.api.responses import APIResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        raise exc
    elif isinstance(response.data, dict):
        errors = [
            VelaitError(name=error_name, description=error_description)
            for error_name, error_description in response.data.items()
        ]
    else:
        errors = response.data

    return APIResponse(
        data=None,
        status=response.status_code,
        template_name=response.template_name,
        headers=response.headers,
        exception=response.exception,
        content_type=response.content_type,
        errors=errors,
    )
