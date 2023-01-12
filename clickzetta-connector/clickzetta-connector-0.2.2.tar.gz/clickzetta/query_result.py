import io
import string
import base64
import numpy
import csv
import decimal


class QueryData(object):
    def __init__(self, data: list):
        self.data = data

    def fetch_one(self) -> string:
        if len(self.data):
            return self.data[0]
        return []

    def fetch_many(self, size: int) -> list:
        if len(self.data):
            if size > len(self.data):
                return self.data
            else:
                return self.data[0:size]
        return []

    def fetch_all(self):
        return self.data


class Field(object):
    def __init__(self):
        self.name = None
        self.field_type = None
        self.precision = None
        self.scale = None
        self.length = None
        self.nullable = None

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.field_type = type

    def set_precision(self, precision):
        self.precision = precision

    def set_scale(self, scale):
        self.scale = scale

    def set_length(self, length):
        self.length = length

    def set_nullable(self, nullable):
        self.nullable = nullable


class QueryResult(object):
    def __init__(self, total_msg: string, query_type: str):
        self.data = None
        self.state = None
        self.total_row_count = 0
        self.total_msg = total_msg
        self.schema = []
        self.query_type = query_type
        self._parse_result_data()

    def _parse_field(self, field: str, schema_field: Field):
        schema_field.set_name(field['name'])
        if field['type'].__contains__('charTypeInfo'):
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) != 'False')
            schema_field.set_length(field['type']['charTypeInfo']['length'])
        elif field['type'].__contains__('decimalTypeInfo'):
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) == 'true')
            schema_field.set_precision(field['type']['decimalTypeInfo']['precision'])
            schema_field.set_scale(field['type']['decimalTypeInfo']['scale'])
        else:
            schema_field.set_type(field['type']['category'])
            schema_field.set_nullable(str(field['type']['nullable']) == 'true')

    def get_result_state(self) -> string:
        return self.total_msg['status']['state']

    def _parse_result_data(self):
        if self.query_type == 'anon':
            field = Field()
            field.set_name('RESULT_MESSAGE')
            field.set_type("STRING")
            self.schema.append(field)
            self.total_row_count = 1
            result_data = [['OPERATION SUCCEED']]
            self.data = QueryData(result_data)
            return
        self.state = self.total_msg['status']['state']
        if self.state != 'FAILED':
            if self.query_type == 'create' or self.query_type == 'alter' or self.query_type == 'drop' or self.query_type == 'truncate' or self.query_type == 'insert':
                field = Field()
                field.set_name('RESULT_MESSAGE')
                field.set_type("STRING")
                self.schema.append(field)
                self.total_row_count = 1
                result_data = [['OPERATION SUCCEED']]
                self.data = QueryData(result_data)
            else:
                if not (len(self.total_msg['resultSet']['data']['data'])):
                    self.total_row_count = 0
                    fields = self.total_msg['resultSet']['metadata']['fields']
                    for field in fields:
                        schema_field = Field()
                    self._parse_field(field, schema_field)
                    self.schema.append(schema_field)
                    self.data = QueryData([])
                    return
                result_data = self.total_msg['resultSet']['data']['data'][0]
                data_list = []
                if len(result_data):
                    decode_data = base64.b64decode(result_data).strip().decode('utf-8')
                    data_list = decode_data.split('\n')
                self.total_row_count = len(data_list)
                fields = self.total_msg['resultSet']['metadata']['fields']
                for field in fields:
                    schema_field = Field()
                    self._parse_field(field, schema_field)
                    self.schema.append(schema_field)
                result_data = []
                csv.register_dialect('cz_dialect', delimiter=',', escapechar='\\')
                for row in data_list:
                    data_list = []
                    if self.query_type == 'select' or self.query_type == 'desc':
                        reader = csv.reader(io.StringIO(row), dialect='cz_dialect')
                        for line in reader:
                            for i in range(len(line)):
                                if self.schema[i].field_type.startswith('DECIMAL') or \
                                        self.schema[i].field_type.startswith('decimal'):
                                    if line[i] == "\\N":
                                        data_list.append("NULL")
                                    else:
                                        data_list.append(decimal.Decimal(line[i]))
                                elif self.schema[i].field_type.startswith('INT') or \
                                        self.schema[i].field_type.startswith('int'):
                                    if line[i] == "\\N":
                                        data_list.append("NULL")
                                    else:
                                        data_list.append(int(line[i]))
                                elif self.schema[i].field_type.startswith('FLOAT') or \
                                        self.schema[i].field_type.startswith('float'):
                                    if line[i] == "\\N":
                                        data_list.append("NULL")
                                    else:
                                        data_list.append(float(line[i]))
                                else:
                                    data_list.append(line[i])
                        if len(data_list) > len(self.schema):
                            data_list = data_list[0:len(self.schema)]
                    elif self.query_type == 'show':
                        if len(self.schema) == 1:
                            data_list.append(row)
                        else:
                            for value in row.split(','):
                                data_list.append(value)
                            if len(data_list) > len(self.schema):
                                data_list = data_list[0:len(self.schema)]
                    else:
                        data_list.append(row)
                    result_data.append(data_list)
                self.data = QueryData(result_data)
        else:
            field = Field()
            field.set_name('ERROR_MESSAGE')
            field.set_type("STRING")
            self.schema.append(field)
            self.total_row_count = 1
            result_data = [[self.total_msg['status']['message']]]
            self.data = QueryData(result_data)
