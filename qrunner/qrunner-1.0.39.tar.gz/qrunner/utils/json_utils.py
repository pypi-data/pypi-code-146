"""
genson:
https://github.com/wolverdude/GenSON
"""
import json
from genson import SchemaBuilder
from qrunner.utils.log import logger


def formatting(msg):
    """formatted message"""
    if isinstance(msg, dict):
        return json.dumps(msg, indent=2, ensure_ascii=False)
    return msg


def get_schema(data: dict = None):
    """
    return schema data
    """
    builder = SchemaBuilder()
    builder.add_object(data)
    to_schema = builder.to_schema()
    to_schema.pop('$schema')
    logger.debug(f'生成schmea如下:\nschema start-------------->\n{formatting(to_schema)}\nschema end-------------->')
    return to_schema

