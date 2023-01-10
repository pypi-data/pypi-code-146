from jupyter_server.utils import url_path_join

from low_code_assistant.jupyter.mixpanel_handler import MixpanelHandler


def _jupyter_server_extension_paths():
    return [{"module": "low_code_assistant.jupyter.server_extension"}]


def _load_jupyter_server_extension(server_app):
    web_app = server_app.web_app

    host_pattern = ".*$"
    base_url = url_path_join(web_app.settings["base_url"])

    web_app.add_handlers(
        host_pattern,
        [
            (url_path_join(base_url, "/mixpanel/(.*)"), MixpanelHandler, {}),
        ],
    )


# For backward compatibility
load_jupyter_server_extension = _load_jupyter_server_extension
