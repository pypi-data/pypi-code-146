class DynamoDBValues:
    PARTITION_KEY = "primary_identifier"
    TABLE_NAME = "aut-cf-customizations"


class RowColumnNames:
    """
    Constants
    """

    # Doubles as the Partition Key for Dynamo DB
    PRIMARY_IDENTIFIER_NAME = "primary_identifier"

    STACK_NAME = "stack_identifier"
    MODEL_NAME = "current_model"
    RESOURCE_NAME = "logical_resource_id"
    LASTUPDATED_NAME = "last_updated"
    TYPE_NAME = "type_name"
