# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from xmlhelpy import Choice
from xmlhelpy import option
from xmlhelpy import Path

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import search_pagination_options
from kadi_apy.cli.main import kadi_apy


@kadi_apy.group()
def templates():
    """Commands to manage templates."""


@templates.command()
@apy_command
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the template.",
    default=None,
)
@option("title", char="t", description="Title of the template.")
@option(
    "type",
    char="y",
    description="Type of the template.",
    param_type=Choice(["extras", "record"]),
    default="record",
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned template id.",
    is_flag=True,
)
@option(
    "data",
    char="d",
    description="Data for the template.",
    default=None,
)
@option(
    "exit-not-created",
    char="e",
    description="Exit with error if the template was not newly created.",
    is_flag=True,
)
def create(manager, **kwargs):
    """Create a template."""

    if kwargs["data"] is None:
        if kwargs["type"] == "record":
            kwargs["data"] = {}
        else:
            kwargs["data"] = []

    manager.template(create=True, **kwargs)


@templates.command()
@apy_command
@id_identifier_options(class_type="template", helptext="to delete.")
@option(
    "i-am-sure", description="Enable this option to delete the template.", is_flag=True
)
def delete(template, i_am_sure):
    """Delete a template."""

    template.delete(i_am_sure)


@templates.command()
@apy_command
@search_pagination_options
def get_templates(manager, **kwargs):
    """Search for templates."""

    search = manager.search_resource()

    search.search_resources("template", **kwargs)


@templates.command()
@apy_command
@id_identifier_options(class_type="template", helptext="to edit.")
@option(
    "visibility",
    char="v",
    description="Visibility of the template to set.",
    default=None,
    param_type=Choice(["private", "public"]),
)
@option("title", char="i", default=None, description="Title of the template to set.")
@option(
    "description",
    char="d",
    default=None,
    description="Description of the template to set.",
)
def edit(template, visibility, title, description):
    """Edit the metadata of a template."""

    template.set_attribute(visibility=visibility, title=title, description=description)


@templates.command()
@apy_command
@id_identifier_options(class_type="template", helptext="to export.")
@option(
    "export_type",
    char="e",
    description="Export type.",
    default="json",
    param_type=Choice(["json", "json-schema"]),
)
@option(
    "path",
    char="p",
    description="Path (folder) to store the file.",
    param_type=Path(exists=True),
    default=".",
)
@option(
    "name",
    char="n",
    description="Name of the file to store. The identifier is used as default.",
)
@option(
    "force",
    char="f",
    description="Enable if existing file with identical name should be replaced.",
    is_flag=True,
)
@option(
    "pipe",
    char="P",
    description="Use this flag if you want to pipe the returned json.",
    is_flag=True,
)
@option(
    "use-folder",
    char="u",
    description="Create, if not already existing, a folder in the specified file path"
    " with the template's identifier as name and save the exported file in this"
    " folder.",
    is_flag=True,
)
def export(template, export_type, path, name, force, pipe, use_folder):
    """Export the template using a specific export type."""

    template.export(export_type, path, name, force, pipe, use_folder)
