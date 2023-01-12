from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import csv
from cassandra.query import dict_factory
import boto3
import os
import sys
from datetime import datetime
import uuid
from python_cassandra_cli.aws_utils import AWSUtils

client_s3 = boto3.client('s3')

import dotenv

dotenv.load_dotenv()

class RestoreBackupKeyspace(object):

    def __init__(self, s3, id, key, keyspace, region, schema, snapshot_folder, host, user, password,
        ssm_secret, secret_name, drop_keyspace, rows_limit):

        self.s3 = s3
        self.id = id
        self.key = key
        self.keyspace = keyspace
        self.region = region
        self.schema = schema
        self.snapshot_folder = snapshot_folder
        self.host = host
        self.user = user
        self.password = password
        self.ssm_secret = ssm_secret
        self.secret_name = secret_name
        self.drop_keyspace = drop_keyspace
        self.rows_limit = rows_limit

    def restore_backup_keyspace(self) :

        try:

            aws_utils = AWSUtils(self.id, self.key)

            client_s3 = aws_utils.s3_client()

            client_ssm = aws_utils.ssm_client(self.id, self.key, self.region)

            list=client_s3.list_objects(Bucket=self.s3, Prefix=self.snapshot_folder)['Contents']
            
            print('Copying files from s3: ' + self.s3)
            for s3_key in list:
                s3_object = s3_key['Key']
                # creating folder for object
                os.makedirs(os.path.dirname(s3_object), exist_ok=True)
                # copy object from s3 to local folder
                client_s3.download_file(self.s3, s3_object, s3_object)
                print('Downloaded: ' + s3_object)

            # Get user/password credentials
            if self.ssm_secret:
                print('Getting secrets from SSM')
                parameter = client_ssm.get_parameter(Name=self.secret_name, WithDecryption=True)
                value_array = parameter['Parameter']['Value'].split('\n')
                result_dict={}
                for item in value_array:
                    result_dict[item.partition('=')[0]]=item.partition('=')[2]
                user=result_dict['USER']
                password=result_dict['PASSWORD']
            else:
                user = str(os.getenv('CASSANDRA_HOST_USER')) or self.user
                password = str(os.getenv('CASSANDRA_HOST_PASSWORD')) or self.password

            host = os.getenv('CASSANDRA_HOST') or self.host

            # connecting to cassandra
            auth_provider = PlainTextAuthProvider(username=user, password=password)
            cluster = Cluster([host], auth_provider=auth_provider, protocol_version=4)

            session = cluster.connect()


            session.row_factory = dict_factory

            if self.schema:
                print('Creating keyspace schema');
                file_schema = open(self.snapshot_folder + '/keyspace_schema.txt', 'r')
                schema = file_schema.readlines()

                schema_dict = []
                for line in schema:
                    schema_dict.append(line)
                schema_str = ''.join(schema_dict)
                schema_stmts = schema_str.split(';')
                schema_stmts = schema_stmts[ : -1]

                if self.drop_keyspace:
                    try:
                        print(f"DROP keyspace {self.keyspace}")
                        session.execute(f"DROP keyspace {self.keyspace}")

                    except Exception as e: 
                        
                        print(e)

                for query in schema_stmts:
                    # create schema
                    if query.find('CREATE TABLE'):
                        query = query.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
                    if query.find('CREATE INDEX'):
                        query = query.replace('CREATE INDEX', 'CREATE INDEX IF NOT EXISTS')
                    if query.find('CREATE INDEX'):
                        query = query.replace('CREATE KEYSPACE', 'CREATE KEYSPACE IF NOT EXISTS')
                    print(query)
                    session.execute(query) 


                
            select_tables_stmt = session.prepare("SELECT * FROM system_schema.tables WHERE keyspace_name=?")

            tables = session.execute(select_tables_stmt, [self.keyspace])
 
            for table in tables:
                table_name=table["table_name"]
                print('Restoring table: ' + table_name)
                file_meta = open(self.snapshot_folder + '/' + table_name + '_table_meta.txt', 'r')
                table_meta = file_meta.readlines()
                # print(table_meta)
                table_meta_dict = []
                values_dict = []
                for line in table_meta:
                    table_meta_dict.append(line.strip())
                    values_dict.append("?")
                if table_meta_dict[0] == "NODATA":

                    print(f"Table {table_name} doesn't have data to restore")

                else:
                    data_count_origin = int(table_meta_dict[-1])
                    # remove last object count
                    table_meta_dict = table_meta_dict[ : -1]
                    values_dict = values_dict[ : -1]
                    result_type_stmt = session.prepare(f"SELECT type from system_schema.columns where table_name = \'{table_name}\' and keyspace_name = \'{self.keyspace}\' and column_name=? allow filtering;")
                    result_kind_stmt = session.prepare(f"SELECT kind from system_schema.columns where table_name = \'{table_name}\' and keyspace_name = \'{self.keyspace}\' and column_name=? allow filtering;")
                    data_types = {}
                    data_types_list = []
                    data_kind_list = []

                    for value_column in  table_meta_dict:
                        result_type = session.execute(result_type_stmt, [value_column])
                        result_kind = session.execute(result_kind_stmt, [value_column])
                        data_types[value_column] = result_type[0]['type']
                        data_types_list.append(result_type[0]['type'])
                        data_kind_list.append(result_kind[0]['kind'])

                    table_meta_str = ','.join(table_meta_dict)
                    values_str = ','.join(values_dict)

                    insert_data_stmt = session.prepare(f"INSERT INTO {self.keyspace}.{table_name} ({table_meta_str}) VALUES ({values_str});")
                    #increase the limit for csv
                    csv.field_size_limit(os.getenv('CSV_FIELD_SIZE_LIMIT') or 100000000)
                    with open(self.snapshot_folder + '/' + table_name + '.csv', newline='') as csvfile:
                        data = csv.reader(csvfile, delimiter='|')
                        for row in data:
                            # print(row)
                            for i in range(len(row)):
                                if row[i] == '':
                                    if data_kind_list[i] not in ('clustering','partition_key'):
                                        row[i] = None
                                elif data_types_list[i] == 'timestamp':
                                    try:
                                        row[i] = datetime.strptime(row[i], '%Y-%m-%d %H:%M:%S')
                                    except Exception as e: 
                                        row[i] = None
                                        print(e)
                                elif data_types_list[i] in ('bigint','int','varint'):
                                        row[i] = int(row[i])
                                elif data_types_list[i] == 'uuid':
                                    try:
                                        row[i] = uuid.UUID(str(row[i]))
                                    except ValueError as e:
                                        row[i] = None
                                        print(e)
                                elif data_types_list[i] == 'boolean':
                                    if row[1] == ('True' or 'true'):
                                        row[i] = True
                                    elif row[1] == ('Fasle' or 'false'):
                                        row[i] = False
                                    else:
                                        row[i] = None  
                                elif data_types_list[i] == 'list<text>':
                                    row[i] = row[i].split(",")
                                elif data_types_list[i] == 'set<text>':
                                    if row[i].startswith("{"):
                                        row[i] = row[i][1:]
                                    if row[i].endswith("}"): 
                                        row[i] = row[i][1:]
                                    row[i] =row[i].replace("'","").split(",")
                                    row[i] = set([item.strip() for item in row[i]])

                            session.execute(insert_data_stmt, row)

                    rows_count = session.execute(f"SELECT * from {self.keyspace}.{table_name} LIMIT {self.rows_limit}")

                    data_count_current = 0
                    for row in rows_count:
                        data_count_current += 1
                   

                    print(f"Data count in table {table_name} origin equal {data_count_origin}")
                    print(f"Data count in table {table_name} current equal {data_count_current}")
        except Exception as e: 
            print(e)
            sys.exit(1)
