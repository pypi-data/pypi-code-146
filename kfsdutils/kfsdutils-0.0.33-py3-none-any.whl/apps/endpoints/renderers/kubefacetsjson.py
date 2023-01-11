"""
Provides JSON rendering support.
"""
from __future__ import unicode_literals
import json

from rest_framework.renderers import BaseRenderer
from kfsdutils.apps.endpoints.handlers.core.yaml import Yaml


class KubefacetsJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    """

    media_type = "application/json"
    format = "json"
    charset = "utf-8"
    ensure_ascii = False
    default_flow_style = False

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized JSON.
        """
        if data is None:
            return ""
        customYaml = Yaml()
        try:
            formattedData = customYaml.getPythonObj(customYaml.formatDictConfig(data))
            jsonIndented = json.dumps(formattedData, indent=4)
            return jsonIndented
        except Exception:
            return json.dumps(data, indent=4)
