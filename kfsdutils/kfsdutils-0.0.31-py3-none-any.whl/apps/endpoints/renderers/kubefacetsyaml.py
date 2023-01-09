"""
Provides YAML rendering support.
"""
from __future__ import unicode_literals
import json

from rest_framework.renderers import BaseRenderer
from kfsdutils.apps.endpoints.handlers.core.yaml import Yaml
import yaml


class KubefacetsYAMLRenderer(BaseRenderer):
    """
    Renderer which serializes to YAML.
    """

    media_type = "application/yaml"
    format = "yaml"
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized YAML.
        """

        customYaml = Yaml()
        if data is None:
            return ""

        renderer_context = renderer_context or {}

        try:
            return customYaml.getYaml(customYaml.formattedValueByType(data))
        except Exception:
            jsonFormat = json.dumps(data)
            dictObj = json.loads(jsonFormat)
            return yaml.dump(dictObj)
