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
# pylint: disable=missing-function-docstring
import os
from functools import reduce

from authlib.common.urls import add_params_to_qs
from flask import Blueprint
from flask import current_app
from flask import render_template
from flask_babel import gettext as _
from werkzeug.datastructures import MultiDict

from . import DEFAULT_URL
from . import PLUGIN_NAME
from .utils import CollectionZenodoForm
from .utils import FileStreamGenerator
from .utils import RecordZenodoForm
from .utils import UploadCanceledException
from .utils import ZipStreamGenerator
from kadi.lib.conversion import markdown_to_html
from kadi.lib.licenses.utils import get_builtin_licenses
from kadi.lib.resources.utils import get_linked_resources
from kadi.modules.records.export import get_export_data
from kadi.plugins import db
from kadi.plugins import get_plugin_config
from kadi.plugins import hookimpl
from kadi.plugins import open_file
from kadi.plugins import Record


# Currently only used for the custom template folder.
bp = Blueprint(PLUGIN_NAME, __name__, template_folder="templates")


def _validate_plugin_config(plugin_config):
    if not plugin_config.get("client_id") or not plugin_config.get("client_secret"):
        current_app.logger.error(
            f"Missing client ID and/or secret in '{PLUGIN_NAME}' plugin."
        )
        return False

    return True


@hookimpl
def kadi_register_blueprints(app):
    app.register_blueprint(bp)


@hookimpl
def kadi_get_translations_paths():
    return os.path.join(os.path.dirname(__file__), "translations")


def _compliance_fix(session):
    def _refresh_token_request(url, headers, body):
        # Zenodo requires sending the client ID and secret each time a token is
        # requested, even for the refresh token grant type.
        plugin_config = get_plugin_config(PLUGIN_NAME)

        client_id = plugin_config["client_id"]
        client_secret = plugin_config["client_secret"]

        body = add_params_to_qs(
            body, {"client_id": client_id, "client_secret": client_secret}
        )
        return url, headers, body

    session.register_compliance_hook("refresh_token_request", _refresh_token_request)


@hookimpl
def kadi_register_oauth2_providers(registry):
    plugin_config = get_plugin_config(PLUGIN_NAME)

    if not _validate_plugin_config(plugin_config):
        return

    client_id = plugin_config["client_id"]
    client_secret = plugin_config["client_secret"]
    base_url = plugin_config.get("base_url", DEFAULT_URL)

    registry.register(
        name=PLUGIN_NAME,
        client_id=client_id,
        client_secret=client_secret,
        access_token_url=f"{base_url}/oauth/token",
        access_token_params={"client_id": client_id, "client_secret": client_secret},
        authorize_url=f"{base_url}/oauth/authorize",
        api_base_url=f"{base_url}/api/",
        client_kwargs={"scope": "deposit:write"},
        compliance_fix=_compliance_fix,
    )


@hookimpl
def kadi_get_oauth2_providers():
    plugin_config = get_plugin_config(PLUGIN_NAME)

    if not _validate_plugin_config(plugin_config):
        return None

    return {
        "name": PLUGIN_NAME,
        "title": "Zenodo",
        "website": plugin_config.get("base_url", DEFAULT_URL),
        "description": render_template("zenodo/description_oauth.html"),
    }


@hookimpl
def kadi_get_publication_providers(resource):
    return {
        "name": PLUGIN_NAME,
        "description": render_template(
            "zenodo/description_publication.html",
            resource_type=resource.__class__.__tablename__,
        ),
    }


@hookimpl
def kadi_get_publication_form(provider, resource):
    if provider != PLUGIN_NAME:
        return None

    if isinstance(resource, Record):
        form = RecordZenodoForm()
    else:
        form = CollectionZenodoForm()

    return render_template("zenodo/publication_form.html", form=form, resource=resource)


def _delete_deposit(deposit, client, token):
    try:
        client.delete(deposit["links"]["self"], token=token)
    except:
        pass


def _make_error_template(message=None, response=None):
    status = response.status_code if response is not None else None

    if message is None:
        try:
            # If the email address of the account is not confirmed yet, no deposits can
            # be created. Unfortunately, Zenodo only returns an HTML response in this
            # case, so we try to catch that.
            if (
                response.status_code == 403
                and response.headers["Content-Type"] == "text/html; charset=utf-8"
            ):
                message = _("Please verify your email address first.")
            else:
                message = response.json()["message"]
        except:
            message = _("Unknown error.")

    return render_template("zenodo/upload_error.html", message=message, status=status)


def _upload_error(response, deposit, client, token):
    _delete_deposit(deposit, client, token)
    return False, _make_error_template(response=response)


@hookimpl
def kadi_publish_resource(provider, resource, form_data, user, client, token, task):
    if provider != PLUGIN_NAME:
        return None

    # Zenodo requires at least 4 characters for the description.
    description = (
        resource.description if len(resource.description) >= 4 else "*No description.*"
    )
    # The basic metadata to use independent of resource type.
    json_data = {
        "metadata": {
            "upload_type": "dataset",
            "title": resource.title,
            "creators": [{"name": user.identity.displayname}],
            "description": markdown_to_html(description),
            "license": "CC-BY-4.0",
            "keywords": [tag.name for tag in resource.tags.order_by("name")],
        }
    }

    if isinstance(resource, Record):
        form = RecordZenodoForm(formdata=MultiDict(form_data))

        # If applicable, add the existing license of a record, as long as it is a
        # built-in license, as these are the only ones Zenodo supports.
        if resource.license:
            builtin_licenses = get_builtin_licenses()

            if resource.license.name in builtin_licenses:
                json_data["metadata"]["license"] = resource.license.name
    else:
        form = CollectionZenodoForm(formdata=MultiDict(form_data))

    if not form.validate():
        return False, render_template("zenodo/validation_error.html", form=form)

    deposit = None
    export_types = []

    if form.export_type.data:
        export_types = (
            [form.export_type.data]
            if form.export_type.data != "both"
            else ["json", "pdf"]
        )

    try:
        # Create a new deposit using the JSON metadata, which we can then use for
        # uploading files.
        response = client.post("deposit/depositions", token=token, json=json_data)

        if response.status_code != 201:
            return False, _make_error_template(response=response)

        deposit = response.json()
        bucket_url = deposit["links"]["bucket"]

        # Package the uploaded data. For records, a single ZIP archive is created
        # containing all files and exported data. For collections, a single ZIP archive
        # is created containing a folder for each record with the same data as for
        # record uploads.
        if form.package_data.data:
            if isinstance(resource, Record):
                records = resource
            else:
                records = get_linked_resources(Record, resource.records, user=user)

            stream = ZipStreamGenerator(
                records, export_types, form.export_filter.data, user, task
            )
            response = client.put(
                f"{bucket_url}/{resource.identifier}.zip", token=token, data=stream
            )

            if response.status_code != 200:
                return _upload_error(response, deposit, client, token)

        # Do not package the uploaded data. For records, all files and exported data are
        # uploaded individually. For collections, a ZIP archive is created for each
        # record containing all files and exported data of the record.
        else:
            if isinstance(resource, Record):
                num_files = resource.active_files.count()

                for index, file in enumerate(resource.active_files):
                    # Ignore empty files.
                    if file.size == 0:
                        continue

                    with open_file(file) as f:
                        stream = FileStreamGenerator(f, file.size, task)
                        response = client.put(
                            f"{bucket_url}/{file.name}", token=token, data=stream
                        )

                        if response.status_code != 200:
                            return _upload_error(response, deposit, client, token)

                        if task is not None:
                            # This is not nearly as accurate as using the size of each
                            # file (and does not include potential export data), but it
                            # should suffice for rough progress indication.
                            task.update_progress((index + 1) / num_files * 100)
                            db.session.commit()

                for export_type in export_types:
                    export_data = get_export_data(
                        resource,
                        export_type,
                        export_filter=form.export_filter.data,
                        user=user,
                    )
                    response = client.put(
                        f"{bucket_url}/{resource.identifier}.{export_type}",
                        token=token,
                        data=export_data,
                    )

                    if response.status_code != 200:
                        return _upload_error(response, deposit, client, token)
            else:
                streams = []
                records = get_linked_resources(Record, resource.records, user=user)

                for record in records:
                    stream = ZipStreamGenerator(
                        record,
                        export_types,
                        form.export_filter.data,
                        user,
                        task,
                        update_task=False,
                    )
                    streams.append((record.identifier, stream))

                total_size = reduce(lambda a, b: a + len(b[1]), streams, 0)

                for identifier, stream in streams:
                    response = client.put(
                        f"{bucket_url}/{identifier}.zip", token=token, data=stream
                    )

                    if response.status_code != 200:
                        return _upload_error(response, deposit, client, token)

                    if task is not None:
                        task.update_progress(len(stream) / total_size * 100)
                        db.session.commit()

    except UploadCanceledException:
        _delete_deposit(deposit, client, token)
        return False, _("Upload canceled.")

    except Exception as e:
        if deposit is not None:
            _delete_deposit(deposit, client, token)

        return False, _make_error_template(message=repr(e))

    return True, render_template(
        "zenodo/upload_success.html", deposit_url=deposit["links"]["html"]
    )
