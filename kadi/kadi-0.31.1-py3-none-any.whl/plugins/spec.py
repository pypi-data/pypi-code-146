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
from pluggy import HookspecMarker


hookspec = HookspecMarker("kadi")


@hookspec
def kadi_register_blueprints(app):
    """Hook for registering custom Flask blueprints.

    An example Flask blueprint may look like the following:

    .. code-block:: python3

        from flask import Blueprint

        bp = Blueprint(
            'my_plugin',
            __name__,
            url_prefix='/my_plugin',
            template_folder='templates',
            static_folder='static',
        )

    The optional parameters of this example blueprint specify a custom URL prefix, a
    folder for HTML templates and a folder for static files, respectively. The template
    and static folders should be relative to the blueprint's root path. In this example,
    static files will be accessible using the path ``/my_plugin/static/<filename>``.

    Note that since API endpoints are handled a bit differently in the application, the
    existing API blueprint (using ``api`` as name and ``/api`` as URL prefix) should be
    used for custom API endpoints. An example on how to use it may look like the
    following:

    .. code-block:: python3

        from kadi.plugins import api_bp
        from kadi.plugins import json_response

        @api_bp.get("/my_plugin/<my_endpoint>")
        def my_endpoint():
            return json_response(200)

    :param app: The application object, which is used to register the blueprint via
        its ``register_blueprint`` method.
    """


@hookspec
def kadi_get_scripts():
    """Hook for collecting script URLs.

    Each plugin can return a string or a list of strings, each string representing the
    full URL where the script can be loaded from. As only internal scripts can currently
    be used, scripts should be loaded via a custom static route, which a plugin can
    define by using :func:`kadi_register_blueprints`.

    The scripts are inserted on every page by default, however, plugins may limit each
    script to certain pages based on e.g. the current endpoint (``request.endpoint``) or
    other requirements. In case no script should be inserted, the plugin has to return
    ``None``.

    Note that the scripts are inserted into the HTML body right before the main template
    content. An example of using this hook would be the registration of custom (global)
    Vue.js components, which can be used in combination with a template such as the one
    shown in :func:`kadi_get_preview_templates`:

    .. code-block:: js

        Vue.component('my-previewer-component', {
            // The data to preview. Its type depends on how the preview data is returned
            // from the backend.
            props: {
                data: String,
            },
            // Note the custom delimiters, which are used so they can coexist with
            // Jinja's templating syntax when not using single file components.
            template: `
                <div>{$ data $}</div>
            `,
        })
    """


@hookspec
def kadi_register_capabilities():
    """Hook for registering capabilities of a Kadi instance.

    A capability can be e.g. an installed external program or a database extension,
    which may be a requirement for plugins or internal Kadi features to work.

    Either a single or a list of strings, uniquely representing the capabilities can be
    returned. If the requirements for none of the capabilities are met, ``None`` can be
    returned instead.
    """


@hookspec
def kadi_get_storages():
    """Experimental hook for collecting storage providers.

    Either a single storage or a list of storages can be returned by each plugin. Each
    storage must be a concrete instance of a class derived from :class:`.BaseStorage`
    with a unique storage type.
    """


@hookspec
def kadi_get_translations_paths():
    """Hook for collecting translation paths used for backend translations.

    Each translation path must be absolute and needs to contain all configuration and
    message catalog files required by the ``Babel``/``Flask-Babel`` Python libraries.
    The Kadi CLI contains some utility commands to help with creating and managing these
    files:

    .. code-block:: bash

        kadi i18n --help

    Note that translations of the main application always take precedence.

    For adding custom frontend translations, please see
    :func:`kadi_get_translations_bundles`.
    """


@hookspec
def kadi_get_translations_bundles(locale):
    """Hook for collecting translations bundles used for frontend translations.

    Each bundle should consist of a dictionary, mapping the texts to translate to their
    corresponding translated values according to the given locale. This dictionary may
    also be constructed by loading an external JSON file, containing the actual
    translations.

    If a certain locale should be ignored, ``None`` can be returned instead. The same
    can be done to limit the translations to certain pages based on e.g. the current
    endpoint (``request.endpoint``) or other requirements.

    The translations can then be used by calling the globally available ``$t`` function
    with the corresponding text to translate:

    .. code-block:: js

        const translatedText = $t('My translated text');

    This can be combined with custom scripts registered via
    :func:`kadi_get_scripts`, including the use in custom Vue.js components.

    Note that the texts to translate will themselves be used as a fallback if no
    corresponding translation can be found. Therefore, it is recommended to keep these
    texts in english, like in the example above, as english is used as the default
    locale in the application and will therefore need no further handling. Also note
    that translations of the main application always take precedence.

    For adding custom backend translations, please see
    :func:`kadi_get_translations_paths`.

    :param locale: The locale for which translations are collected, currently one of
        ``"en"`` or ``"de"``.
    """


@hookspec
def kadi_get_licenses():
    """Hook for collecting custom licenses.

    All licenses have to be returned as a dictionary, mapping the unique name of a
    license to another dictionary, containing its title and an optional url further
    describing the license.

    An example dictionary may look like the following:

    .. code-block:: python3

        {
            "my_license": {
                "title": "My license",
                # Specifying an URL is optional, but recommended.
                "url": "https://example.com",
            },
        }

    Before any custom licenses can be used, they have to be added to the database. This
    can be done using the Kadi CLI, which also allows updating and/or deleting licenses
    that have been added previously:

    .. code-block:: bash

        kadi db licenses --help
    """


@hookspec
def kadi_get_preferences_config():
    """Hook for collecting configuration needed for plugin-specific preferences.

    Plugin preferences are shown in a separate tab on the user's preferences page. For
    adding a custom preferences tab, a plugin has to return a dictionary containing a
    title, form and a callable returning a template.

    The form should be an instance of a class derived from
    :class:`.PluginConfigForm` containing the unique name of the plugin, while the
    template returned by the callable should only contain the rendering of the form
    fields, since the surrounding form element, including the CSRF input field and the
    submit buttom, are added automatically.

    An example may look like the following:

    .. code-block:: python3

        from flask import render_template
        from kadi.plugins import PluginConfigForm
        from kadi.plugins import StringField

        class MyPluginForm(PluginConfigForm):
            my_field = StringField("My field")

        @hookimpl
        def kadi_get_preferences_config():
            form = MyPluginForm("my_plugin")
            return {
                "title": "My Plugin",
                "form": form,
                "get_template": lambda: render_template(
                    "my_plugin/preferences.html", form=form
                ),
            }
    """


@hookspec
def kadi_register_oauth2_providers(registry):
    """Hook for registering OAuth2 providers.

    Currently, only the authorization code grant type is supported. Each provider needs
    to register itself to the given registry provided by the ``Authlib`` Python library
    using a unique name.

    Needs to be used together with :func:`kadi_get_oauth2_providers`.

    :param registry: The OAuth2 provider registry, which is used to register the
        provider via its ``register`` method.
    """


@hookspec
def kadi_get_oauth2_providers():
    """Hook for collecting OAuth2 providers.

    Each OAuth2 provider has to be returned as a dictionary containing all necessary
    information about the provider. A provider must at least provide the unique name
    that was also used to register it.

    An example dictionary may look like the following:

    .. code-block:: python3

        {
            "name": "my_provider",
            "title": "My provider",
            "website": "https://example.com",
            "description": "The (HTML) description of the OAuth2 provider.",
        }

    Needs to be used together with :func:`kadi_register_oauth2_providers`.
    """


@hookspec
def kadi_get_publication_providers(resource):
    """Hook for collecting publication providers.

    Each publication provider has to be returned as a dictionary containing all
    necessary information about the provider. A provider must at least provide the
    unique name that was also used to register the OAuth2 provider that this provider
    should use. The given resource can be used to adjust the returned information based
    on the resource type.

    An example dictionary may look like the following:

    .. code-block:: python3

        {
            "name": "my_provider",
            "description": "The (HTML) description of the publication provider.",
        }

    Needs to be used together with :func:`kadi_register_oauth2_providers` and
    :func:`kadi_get_oauth2_providers`.

    :param resource: The :class:`.Record` or :class:`.Collection` to eventually publish.
    """


@hookspec(firstresult=True)
def kadi_get_publication_form(provider, resource):
    """Hook for collecting a publication form template of a specific provider.

    Each plugin has to check the given provider and type of the given resource to decide
    whether it should return a form template or not, otherwise it has to return
    ``None``. The template should only contain the rendering of the form fields, since
    the surrounding form element, including the CSRF input field and the submit buttom,
    are added automatically.

    The request data obtained via the form will be passed into the
    :func:`publish_resource` hook as ``form_data``, where it may be used to further
    customize the publication process.

    Needs to be used together with :func:`publish_resource`. Note that the hook chain
    will stop after the first returned result that is not ``None``.

    :param provider: The unique name of the publication provider.
    :param resource: The :class:`.Record` or :class:`.Collection` to eventually publish.
    """


@hookspec(firstresult=True)
def kadi_publish_resource(provider, resource, form_data, user, client, token, task):
    """Hook for publishing a resource using a specific provider.

    Each plugin has to check the given provider and decide whether it should start the
    publishing process, otherwise it has to return ``None``. After finishing the
    publishing process, the plugin has to return a tuple consisting of a flag indicating
    whether the operation succeeded and a (HTML) template further describing the result
    in a user-readable manner, e.g. containing a link to view the published result if
    the operation was successful.

    Needs to be used together with :func:`kadi_get_publication_providers`. Note that the
    hook chain will stop after the first returned result that is not ``None``.

    :param provider: The unique name of the publication provider.
    :param resource: The :class:`.Record` or :class:`.Collection` to publish.
    :param form_data: Form data as dictionary to customize the publication process, see
        :func:`kadi_get_publication_form`.
    :param user: The :class:`.User` who started the publication process.
    :param client: The OAuth2 client to use for authenticated requests together with the
        token.
    :param token: The OAuth2 token to use for authenticated requests together with the
        client.
    :param task: A :class:`.Task` object that may be provided if this hook is executed
        in a background task. Can be used to check whether the publishing operation was
        canceled and to update the current progress of the operation via the task.
    """


@hookspec(firstresult=True)
def kadi_get_custom_mimetype(file, base_mimetype):
    """Hook for determining a custom MIME type of a file.

    Each plugin has to check the given base MIME type and decide whether it should try
    determining a custom MIME type or not. Otherwise, it has to return ``None``. The
    returned MIME type should only be based on the content a file actually contains.

    Can be used together with :func:`kadi_get_preview_data`. Note that the hook chain
    will stop after the first returned result that is not ``None``.

    :param file: The :class:`.File` to get the custom MIME type of.
    :param base_mimetype: The base MIME type of the file, based on the actual file
        content, which a plugin can base its decision to return a custom MIME type on.
    """


@hookspec(firstresult=True)
def kadi_get_preview_data(file):
    """Hook for obtaining preview data of a file to be passed to the frontend.

    Each plugin has to check whether preview data should be returned for the given file,
    based on e.g. its storage type, size or MIME types, otherwise it has to return
    ``None``. The preview data must consist of a tuple containing the preview type and
    the actual preview data used for rendering the preview later.

    Should be used together with :func:`kadi_get_preview_templates` and
    :func:`kadi_get_scripts`. Note that the hook chain will stop after the first
    returned result that is not ``None``.

    :param file: The :class:`.File` to get the preview data of.
    """


@hookspec
def kadi_get_preview_templates(file):
    """Hook for collecting templates for rendering preview data.

    Each template should consist of an HTML snippet containing all necessary markup to
    render the preview data. As currently all previews are rendered using Vue.js
    components, the easiest way to include a custom preview is by using such a
    component, which can automatically receive the preview data from the backend as
    shown in the following example:

    .. code-block:: html

        <!-- Check the preview type first before rendering the component. -->
        <div v-if="previewData.type === 'my_plugin_preview_type'">
            <!-- Pass the preview data from the backend into the component. -->
            <my-preview-component :data="previewData.data"></my-previewer-component>
        </div>

    In order to actually register the custom component via JavaScript,
    :func:`kadi_get_scripts` needs to be used. Should also be used together with
    :func:`kadi_get_preview_data`.

    :param file: The :class:`.File` to get the preview of.
    """


@hookspec
def kadi_post_resource_change(resource, user, created):
    """Hook to run operations after a resource was created or changed.

    Note that the hook is only executed after all changes have been persisted in the
    database and the creation or change triggered the creation of a new revision of the
    given resource. The type of the given resource can be used to react to specific
    changes, while the latest revision of the resource can be retrieved via
    ``resource.ordered_revisions.first()``.

    :param resource: The resource that was created or changed, either a
        :class:`.Record`, :class:`.File`, :class:`.Collection`, :class:`.Template` or
        :class:`.Group`.
    :param user: The :class:`.User` who triggered the creation or change.
    :param created: Flag indicating if the resource was newly created.
    """


@hookspec
def kadi_get_resource_overview_templates(resource):
    """Hook for collecting templates shown on the overview pages of resources.

    The contents collected by this hook will be shown below the existing actions and
    links on the respective resource overview page. For resource types where no
    templates should be collected, ``None`` can be returned instead.

    :param resource: The resource which the overview page belongs to, either a
        :class:`.Record`, :class:`.File`, :class:`.Collection`, :class:`.Template` or
        :class:`.Group`.
    """


@hookspec
def kadi_get_nav_footer_items():
    """Hook for collecting templates for navigation items shown in the footer.

    The contents collected by this hook will be shown on all pages in the footer next to
    the existing navigation items.

    For simple navigation items, without the need for custom styling or translations,
    the ``NAV_FOOTER_ITEMS`` configuration value may also be used instead.
    """


@hookspec
def kadi_get_index_templates():
    """Hook for collecting templates shown on the index page.

    The contents collected by this hook will be shown below the existing content on the
    index page.

    For simple content, consisting of an image and/or markdown text, the ``INDEX_IMAGE``
    and ``INDEX_TEXT`` configuration values may also be used instead.
    """


@hookspec
def kadi_get_about_templates():
    """Hook for collecting templates shown on the about page.

    The contents collected by this hook will be shown below the existing content on the
    about page.
    """
