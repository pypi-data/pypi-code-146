# variable_views.py
#
#   These are views that are used for managing variables
#

from django.shortcuts import render
from psu_base.services import utility_service, message_service, validation_service
from psu_base.decorators import require_authority
from psu_base.models.variable import Variable
from django.http import HttpResponseForbidden, HttpResponse
from psu_base.classes.Log import Log

log = Log()
allowable_role_list = ["~power_user", "variable"]


@require_authority(allowable_role_list)
def variable_list(request):
    """
    List all variables for this application
    """
    # Get all variables
    variables = Variable.objects.filter(app_code=utility_service.get_app_code()).order_by("code")

    return render(
        request,
        "psu_base/variables/list.html",
        {
            "variables": variables
        },
    )


@require_authority(allowable_role_list)
def update_variable(request):
    variable_id = request.POST.get("id")
    prop = request.POST.get("prop")
    val = request.POST.get("value")
    log.trace([id, prop, val])

    # Get targeted variable
    variable_instance = Variable.get(variable_id)

    # Validate property
    # Not allowing data_type to be edited here.  Rather, update it at the code
    # level and delete any saved instance (to be recreated with the new data-type)
    allowed_properties = ['value', 'title']
    if prop not in allowed_properties:
        message_service.post_error(f"Invalid variable property: {prop}")
        return HttpResponseForbidden()

    # Variable values should not contain HTML
    # (use infotext plugin if HTML is required)
    val = validation_service.remove_html(val)

    log.info(f"Change {variable_instance.code} {prop} to {val}")

    if prop == "value":
        if variable_instance.set_value(val):
            return HttpResponse(variable_instance.value)
    else:
        try:
            setattr(variable_instance, prop, val)
            # Do not update the version on changes other than value
            variable_instance.save()
            return HttpResponse(val)
        except Exception as ee:
            log.warning(ee)
            message_service.post_error(f"Unable to update {prop} of {variable_instance.code}")

    return HttpResponseForbidden()


@require_authority(allowable_role_list)
def delete_variable(request):
    log.trace()

    # Get targeted variable
    variable_id = request.POST.get("id")
    variable_instance = Variable.get(variable_id)
    if variable_instance:
        variable_instance.delete()
        return HttpResponse("success")
    else:
        return HttpResponseForbidden()
