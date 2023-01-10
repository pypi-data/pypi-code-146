import os
import boto3
from boto3.dynamodb.conditions import Key

class Tkdynamodb():
    def __init__(self, region=None):
        """
        :param region: The region for AWS S3
        """
        self.service_name = 'dynamodb'
        if region is None:
            region = os.getenv("DYNAMODB_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60

    def get_client(self):
        """
        To be used internally for the purpose of creating the boto3 client of dynamodb.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_resource(self):
        """
        To be used internally for the purpose of creating the boto3 resource of dynamodb.
        This method creates the boto3 resource for AWS, The resource can later be accessed using 'self.resource'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def scan_all(self, table_name, limit=100):
        """
        To be used to Scan the Entire table, Please use this with caution and do not scan bigger tables
        :param table_name:
        :return: list of data (list of dynamodb items)
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.scan()
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            data.extend(result['Items'])
            if len(data) >= limit:
                return data
        return data

    def insert_item(self, table_name, item):
        """
        To be used to Insert an Item to dynamodb table
        :param table_name: Table into which data is supposed to be inserted
        :param item: DynamoDb item to be inserted.
        :return: Boolean
        """
        try:
            self.get_resource()
            table = self.resource.Table(table_name)
            table.put_item(
                Item=item
            )
            return True
        except Exception as err:
            return False

    def delete_item(self, table_name, item):
        """
        :param table_name: Name of DynamoDb Table
        :param item: DynamoDb Item (Should be an object consisting of PK and SK
        :return: Boolean
        """
        try:
            self.get_resource()
            table = self.resource.Table(table_name)
            table.delete_item(
                Key=item
            )
            return True
        except Exception as err:
            return False

    def scan_item_with_key_value(self, table_name, data_key, data_value):
        """
        Note: This method will run over entire table.
        :param table_name: Name of DynamoDb Table
        :param data_key: key present in dynamodb item
        :param data_value: value of the key in dynamodb item.
        :return: list of data matching the filter expression.
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.scan(
            FilterExpression=Key(data_key).eq(data_value),
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(
                FilterExpression=Key(data_key).eq(data_value),
                ConsistentRead=True,
                ExclusiveStartKey=result['LastEvaluatedKey']
            )
            data.extend(result['Items'])
        return data

    def query_item_with_begin_str(self, table_name, pk, pk_val, sk, sk_beginstr):
        """
        :param table_name: Name of DynamoDb Table
        :param pk: partition key of the table
        :param pk_val: partition key value of the table.
        :param sk: Sort key for any partition
        :param sk_beginstr: Sort key value in any partition which begins with
        :return:
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.query(
            KeyConditionExpression=Key(pk).eq(pk_val) & Key(sk).begins_with(sk_beginstr),
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pk_val) & Key(sk).begins_with(sk_beginstr),
                ExclusiveStartKey=result['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data

    def query_item_with_pk(self, table_name, pk, pk_val):
        """
        :param table_name: Name of DynamoDb Table
        :param pk: partition key of the table
        :param pk_val: partition key value which will be returned.
        :return: list of data with pk=pk_val
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.query(
            KeyConditionExpression=Key(pk).eq(pk_val),
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pk_val),
                ExclusiveStartKey=result['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data

    def get_item_by_key(self, table_name, key):
        """
        :param table_name: Name of DynamoDb Table
        :param key: Key of the item containing the Pk and SK
        :return: dynamodb object
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.get_item(Key=key)
        return result['Item'] if 'Item' in result else {}

    def get_item_with_pk_and_sk(self, table_name, pk, pk_val, sk, sk_val):
        """
        Another way to do the same thing is get_item_by_key(table_name, key) method
        :param table_name: Name of DynamoDb Table
        :param pk: partition key of the table
        :param pk_val: partition key value of the table.
        :param sk: Sort key for any partition
        :param sk_val: Sort key value in any partition
        :return: Dynamo db object or empty dict
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        response = table.get_item(Key={pk: pk_val, sk: sk_val})
        return response['Item'] if 'Item' in response else {}

    def scan_items_by_expression(self, table_name, expression):
        """
        :param table_name: Name of DynamoDb Table
        :param expression: Expression for Filter Condition
        :return:
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.scan(
            FilterExpression=expression,
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(
                FilterExpression=expression,
                ConsistentRead=True,
                ExclusiveStartKey=result['LastEvaluatedKey']
            )
            data.extend(result['Items'])
        return data

    def batch_write(self, tablename, items_list):
        """
        :param tablename: Name of DynamoDb Table
        :param items_list: List of items to be inserted in the table
        :return: Boolean
        """
        self.get_resource()
        table = self.resource.Table(tablename)
        counter = 0
        with table.batch_writer() as batch:
            print(f"Writing {len(items_list)} items into {tablename} table")
            for item in items_list:
                try:
                    batch.put_item(Item=item)
                    counter += 1
                except Exception as error:
                    print(f"Error inserting item {item}, {error}", end=', ')
        print(f'Added {counter} items to {tablename}')
        return True

    def scan_item_with_projection(self, table_name, expression, projection_expr):
        """
        :param table_name: Name of DynamoDb Table
        :param expression: Expression for Filter Condition
        :param projection_expr: Expression for selecting the columns (in case only selected columns are needed)
        :return:
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.scan(
            FilterExpression=expression,
            ConsistentRead=True,
            ProjectionExpression=projection_expr
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(
                FilterExpression=expression,
                ConsistentRead=True,
                ProjectionExpression=projection_expr,
                ExclusiveStartKey=result['LastEvaluatedKey']
            )
            data.extend(result['Items'])
        return data

    def query_item_with_key_expression(self, table_name, expression):
        """
        This Method will fetch the data based on the key condition
        It will only work with
        :param table_name: Name of DynamoDb Table
        :param expression: Expression for key Condition (Only Pk and Sk)
        :return:
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        result = table.query(
            KeyConditionExpression=expression,
            ConsistentRead=True
        )
        data = result["Items"]
        while 'LastEvaluatedKey' in result:
            result = table.scan(
                KeyConditionExpression=expression,
                ConsistentRead=True,
                ExclusiveStartKey=result['LastEvaluatedKey']
            )
            data.extend(result['Items'])
        return data

    def table_exists(self, table_name):
        """
        :param table_name: Name of DynamoDb Table
        :return: Boolean (True or False)
        """
        self.get_resource()
        try:
            self.resource.Table(table_name).describe()
            return True  # Table exists
        except:
            return False  # Table does not exist

    def tag_table(self, arn, tags_list):
        """
        :param arn: ARN of the dynamo db table
        :param tags_list: [{'Key': 'name', 'Value': 'table'}]
        :return: Boolean (True or False)
        """
        self.get_client()
        if arn is not None:
            self.client.tag_resource(
                ResourceArn=arn,
                Tags=tags_list
            )
            return True
        else:
            return False

    def enable_time_to_live(self, table_name, ttl_key):
        """
        :param table_name: Name of DynamoDb Table
        :param ttl_key: Key which will have TTL enabled.
        :return ttl_response: Response for ttl_update.
        """
        self.get_client()
        ttl_response = self.client.update_time_to_live(
            TableName=table_name,
            TimeToLiveSpecification={
                'Enabled': True,
                'AttributeName': ttl_key
            }
        )
        return ttl_response

    def batch_get_item(self, table_name, keys_list):
        """
        :param table_name: Name of DynamoDb Table
        :param keys_list: List of keys eg : [{"pk": "pk_val", "sk": "sk_val"}]
        :return: List of Items
        """
        self.get_resource()
        response = self.resource.meta.client.batch_get_item(
            RequestItems={
                table_name: {
                    'Keys': keys_list
                }
            }
        )
        return response['Responses'][table_name]

    def batch_save_data(self, table_name, item_list):
        """
        :param table_name: Name of DynamoDb Table
        :param item_list: List of Items to be saved in the table
        :return: Batch Save response.
        """
        self.get_resource()
        table = self.resource.Table(table_name)
        response = []
        with table.batch_writer() as batch:
            for item in item_list:
                res = batch.put_item(Item=item)
                response.append(res)
        return response

    def batch_delete_data(self, table_name, primary_key, partition_key):
        try:
            self.get_resource()
            table = self.resource.Table(table_name)
            scan = table.scan()
            response = []
            with table.batch_writer() as batch:
                for each in scan['Items']:
                    res = batch.delete_item(
                        Key={
                            primary_key: each[primary_key],
                            partition_key: each[partition_key]
                        }
                    )
                    response.append(res)
            return response
        except Exception as err:
            print("Exception occur while deleting table Error: ", err)



