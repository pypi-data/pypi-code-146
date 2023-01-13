import logging

from satosa.micro_services.base import ResponseMicroService

logger = logging.getLogger(__name__)


def coerce_to_boolean(val):
    if val in [True, "y", "yes", "t", "true", "True", "on", "1", 1]:
        return True
    if val in [False, "n", "no", "f", "false", "False", "off", "0", 0]:
        return False
    return None


class AttributeTyping(ResponseMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("AttributeTyping is active")
        self.boolean_attributes = config["boolean_attributes"]

    def process(self, context, data):
        """
        Convert attributes to appropriate types. Unknown values are converted to None.
        :param context: request context
        :param data: the internal request
        """

        for boolean_attribute in self.boolean_attributes:
            if boolean_attribute in data.attributes:
                data.attributes[boolean_attribute] = (
                    [
                        coerce_to_boolean(val)
                        for val in data.attributes[boolean_attribute]
                    ]
                    if isinstance(data.attributes[boolean_attribute], list)
                    else coerce_to_boolean(data.attributes[boolean_attribute])
                )
                if data.attributes[boolean_attribute] is None or (
                    isinstance(data.attributes[boolean_attribute], list)
                    and all(val is None for val in data.attributes[boolean_attribute])
                ):
                    del data.attributes[boolean_attribute]

        return super().process(context, data)
