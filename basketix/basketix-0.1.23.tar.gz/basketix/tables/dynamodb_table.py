"""AWS DynamoDB table module"""

import json
from decimal import Decimal
from typing import Generic, List, Optional, Any, TypeVar

import boto3
from boto3.dynamodb.conditions import ConditionBase, Key, Attr

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON"""
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class ItemNotFound(Exception):
    """No item found"""

T = TypeVar('T')
class DynamoDBTable(Generic[T]):
    """AWS DynamoDB table"""

    def __init__(self, table_name: str, environment: str, hash_key: str, range_key: Optional[str] = None):
        """Init the AWS DynamoDB table"""

        self.environment = environment
        self.table_name = table_name
        self.hash_key = hash_key
        self.range_key = range_key

        self.table_name_dynamodb = self.table_name if environment == 'prod' else f'{self.table_name}-{environment}'
        self.dynamodb = boto3.resource('dynamodb')
        self.dynamodb_client = boto3.client('dynamodb')

        self.table = self.dynamodb.Table(self.table_name_dynamodb)

    def insert(self, data: List[T])-> int:
        """Insert list of data in the table"""

        for item in self._encode_decimal(data):
            self.table.put_item(Item=item)

        return len(data)

    def partial_update(self, data: List[Any]) -> int:
        """Update list of data in the table"""

        for item in self._encode_decimal(data):
            request_key = {self.hash_key: item[self.hash_key]}
            del item[self.hash_key]
            if self.range_key:
                request_key[self.range_key] = item[self.range_key]
                del item[self.range_key]


            detailed_items = [{'key': key, 'value': value, 'attribute_value_id': f':values_{key}'} for key, value in item.items()]
            update_expression = f"""SET {", ".join([f"{d_i['key']} = {d_i['attribute_value_id']}" for d_i in detailed_items])}"""
            expression_attribute_values = {d_i['attribute_value_id']: d_i['value'] for d_i in detailed_items}

            self.table.update_item(
                Key=request_key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )

        return len(data)

    def update(self, data: List[T]) -> int:
        return self.partial_update(data)

    def get(self, value: str) -> T:
        """Get item by key"""

        try:
            return self.query(value=value)[0]
        except KeyError:
            raise ItemNotFound

    def query(self, value: Any, range_key_value: Optional[str] = None, index_name: Optional[str] = None) -> List[T]:
        """
        Query wrapper for DynamoDB table

        @value: can be the value of the hash key or directly a key condition expression
        @range_key_value <optional>: the value of the range key
        @index_name <optional>: name of the index where to make the request
        """

        if issubclass(type(value), ConditionBase):
            return self._query(key_condition_expression=value, index_name=index_name)

        return self._query(value=value, range_key_value=range_key_value, index_name=index_name)

    def _query(self, value: Optional[str] = None, range_key_value: Optional[str] = None,
               key_condition_expression: Optional[Any] = None, index_name: Optional[str] = None) -> List[T]:
        """Querying the table with the hash key (& range key) value(s) or with a key condition expression"""

        if not key_condition_expression:
            key_condition_expression = Key(self.hash_key).eq(value)
            if range_key_value:
                key_condition_expression &= Key(self.range_key).eq(range_key_value)

        args = {'KeyConditionExpression': key_condition_expression}
        if index_name:
            args['IndexName'] = index_name

        response = self.table.query(**args)

        return [json.loads(json.dumps(res, cls=DecimalEncoder)) for res in response['Items']]

    def exists(self, value: str, range_key_value: Optional[str] = None) -> bool:
        """Check if an item exists or not."""

        return len(self.query(value=value, range_key_value=range_key_value)) > 0

    def scan(self, conditions: Optional[List[dict]] = None, conditions_operator: str = '&', projections: Optional[List[str]] = None) -> List[T]:
        """Scan the table and returns results"""

        conditions = conditions if conditions else []
        dynamo_conditions = []
        for condition in conditions:
            value = self._format_value(condition)
            dynamo_conditions.append(f"Attr('{condition['attr']}').{condition['operator']}({value})")

        filter_expressions = eval(conditions_operator.join(dynamo_conditions)) if dynamo_conditions else None
        projection_expression = ','.join(projections) if projections else None

        if projection_expression and filter_expressions:
            response = self.table.scan(ProjectionExpression=projection_expression, FilterExpression=filter_expressions)

        elif projection_expression and not filter_expressions:
            response = self.table.scan(ProjectionExpression=projection_expression)

        elif not projection_expression and filter_expressions:
            response = self.table.scan(FilterExpression=filter_expressions)

        else:
            response = self.table.scan(Select='SPECIFIC_ATTRIBUTES', AttributesToGet=[self.hash_key])

        items = response['Items']

        while 'LastEvaluatedKey' in response:
            if projection_expression and filter_expressions:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'],
                                           ProjectionExpression=projection_expression,
                                           FilterExpression=filter_expressions)

            elif projection_expression and not filter_expressions:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], ProjectionExpression=projection_expression)

            elif not projection_expression and filter_expressions:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=filter_expressions)

            else:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], Select='SPECIFIC_ATTRIBUTES', AttributesToGet=[self.hash_key])

            items.extend(response['Items'])

        return [json.loads(json.dumps(item, cls=DecimalEncoder)) for item in items]

    def _format_value(self, condition: dict):
        """Format the value depending of the operator"""
        if condition['operator'] in ['exists', 'not_exists']:
            return ''

        if condition['operator'] in ['is_in'] or not condition.get('isStringValue', True):
            return condition['value']

        return "'" + condition['value'] + "'"

    def delete_item(self, value: str, range_key_value: Optional[str] = None):
        """Delete an item by his hash key"""

        request_key = {self.hash_key: value}
        if self.range_key and range_key_value:
            request_key[self.range_key] = range_key_value

        self.table.delete_item(Key=request_key)

    def get_all_keys(self) -> list:
        """Returns all hash keys of the table"""

        data = self.scan(projections=[self.hash_key])

        return [d[self.hash_key] for d in data] #type: ignore

    def _encode_decimal(self, data):
        """Encode float to decimal."""
        return json.loads(json.dumps(data), parse_float=Decimal)
