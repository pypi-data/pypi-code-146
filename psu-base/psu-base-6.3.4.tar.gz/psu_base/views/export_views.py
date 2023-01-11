# backup_views.py
#
#   Used for exporting data from AWS database into fixtures for development instances
#

from psu_base.services import utility_service, auth_service, fixture_export_service, message_service
from psu_base.decorators import require_authority
from django.shortcuts import redirect, render
from django.http import HttpResponse
from psu_base.classes.Log import Log
import sys
import inspect
from django.db import models
from django.core import serializers
from django.apps import apps

log = Log()
allowable_role_list = "developer"


@require_authority(allowable_role_list)
def fixture_export_menu(request):
    """
    Select models to export to JSON files
    """
    app_models = fixture_export_service.get_exportable_model_count()
    return render(request, "psu_base/fixture_export/menu.html", {"app_models": app_models})


@require_authority(allowable_role_list)
def fixture_export_action(request):
    """
    Select models to export to JSON files
    """
    selections = request.POST.getlist("app_model")
    if not selections:
        message_service.post_error("You must select some models to export")
        return redirect("psu:export")

    app_models = {}
    for selection in selections:
        if "|" not in selection:
            message_service.post_error("Invalid selection!")
            return redirect("psu:export")

        x = selection.split("|")
        app_name = x[0]
        model_name = x[1]

        if app_name not in app_models:
            app_models[app_name] = []

        app_models[app_name].append(model_name)

    return fixture_export_service.export_models(app_models)
