from __future__ import annotations

from typing import Union, AnyStr, Any

import influxdb_datalogger

from influxdb_querier.tag_operator import TagOperator


class Tag(str):

    """
    Represents a tag in the WHERE-clause for a query to influxdb.
    A tag will look like this example.

    Examples:
        tag = f"\"{tag_key}\" {tag_operator} \'{tag_value}\'"
    """

    def __new__(cls, tag_key: Union[influxdb_datalogger.Tag, AnyStr], tag_value: Any, tag_operator: TagOperator = TagOperator.equal()) -> Tag:

        assert tag_operator is not None, f"'tag_operator' is None. This is not allowed."
        if isinstance(tag_value, (str, int, float)):
            # A single tag value.
            tag = f"\"{tag_key}\" {tag_operator} \'{tag_value}\'"
        elif isinstance(tag_value, (tuple, list)):
            # We got multiple tag values to combine with `OR`.

            # Build a list of multiple tags.
            tags = [f"\"{tag_key}\" {tag_operator} \'{tag_value_item}\'" for tag_value_item in tag_value]
            # Join the list of tags with `OR` between them.
            tag = " OR ".join(tags)
            # Parenthesise the tags to separate them from the rest.
            tag = f"({tag})"
        else:
            raise Exception(f"Unsupported type for {tag_value}")
        obj = super().__new__(cls, tag)
        obj.tag_key = tag_key
        obj.tag_value = tag_value
        obj.tag_operator = tag_operator
        return obj

    @staticmethod
    def build(tag_key: Union[influxdb_datalogger.Tag, AnyStr], tag_value: Any, tag_operator: TagOperator = TagOperator.equal()) -> Tag:
        f"""
        Builds a {Tag} object from some input variables. 
        :param tag_key: Required. The name of the tag in the database.
        :param tag_value: Required. The value for the tag in the database that you want to query for. 
        :param tag_operator: Optional (default is "="). Used to join the two tags together like: "tag_key" = 'tag_value'. 
        :return: {Tag} object based on the input
        """

        return Tag(tag_key, tag_value, tag_operator)
