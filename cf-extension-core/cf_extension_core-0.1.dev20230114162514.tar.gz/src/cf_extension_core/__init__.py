import logging

from cf_extension_core.interface import (  # noqa: F401
    create_resource,
    update_resource,
    delete_resource,
    read_resource,
    list_resource,
    CustomResourceHelpers,
    DynamoTableCreator,
    DynamoDBValues,
    generate_dynamo_resource,
)


def default_package_logging_config() -> None:
    """
    Helps setup default logging config for custom resources
    :return:
    """
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    logging.getLogger(__name__).setLevel(logging.DEBUG)


# Package Logger
# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())
