from tempfile import TemporaryDirectory
from django.http import HttpResponse
from django.shortcuts import render
from django.core.management import call_command
from django_db_schema_renderer.forms import DBSchemaSelectionForm
from urllib.parse import quote

# TODO: Find some pretty svg
SVG = "%3Csvg xmlns='http://www.w3.org/2000/svg' %3E%3Crect width='400' height='300' \
    fill='%23cccccc'%3E%3C/rect%3E%3Ctext %3E400x300%3C/text%3E%3C/svg%3E"


def create_db_schema_graph_model_view(request) -> HttpResponse:
    """
    Renders a checkbox form or an SVG.

    Once the form is submitted, this function creates a temporary output file,
        calls the django extension "graph_models" command, and then sends the
        SVG to the output template.

    Args:
        request (WSGIRequest)

    Returns:
        An HttpResponse object which renders the selection or visualization page.
    """
    if request.method == "POST":
        form = DBSchemaSelectionForm(request.POST)
        if form.is_valid():
            apps = form.cleaned_data["selected_apps"]
            models = form.cleaned_data["selected_models"]
            with TemporaryDirectory() as tmpdir:
                _output_filepath: str = f"{tmpdir}/db_schema.svg"
                # * Empty form render all db schema
                if not apps and not models:
                    call_command(
                        "graph_models",
                        all_applications=True,
                        group_models=True,
                        output=_output_filepath,
                    )
                # * Only apps provided, render all models for apps
                if apps and not models:
                    call_command(
                        "graph_models",
                        apps,
                        group_models=True,
                        output=_output_filepath,
                    )
                # * Only models provided , apps became we must use  all apps to hit models
                if models:
                    call_command(
                        "graph_models",
                        all_applications=True,
                        include_models=models,
                        group_models=True,
                        output=_output_filepath,
                    )
                with open(_output_filepath, "r") as file_svg:
                    svg: str = file_svg.read()
                    svg: str = svg[svg.find("<svg") :]
                    svg: str = svg.replace(' xlink:title="&lt;TABLE&gt;"', "")
                    svg: str = quote(svg)
            return render(request=request, template_name="input.html", context={"form": form, "svg": svg})
    else:
        form = DBSchemaSelectionForm()
    return render(
        request=request,
        template_name="input.html",
        context={
            "form": form,
            "svg": SVG,
        },
    )
