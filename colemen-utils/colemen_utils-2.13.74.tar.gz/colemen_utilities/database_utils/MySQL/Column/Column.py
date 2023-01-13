# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# import json
# import time
from dataclasses import dataclass
# from typing import List
# from typing import Iterable, Union


# import colemen_utils as c

# from apricity_labs import main as _main
# import apricity.settings as _settings
# import apricity.objects.Validator as _valid
# import apricity.objects.Token as _token
# import apricity.objects.Result as _result
# import apricity.objects.Log as log
# from apricity.susurrus.request import Request
# from settings.types import _Union
from colemen_config import _db_column_type,_db_column_sql_data_type,_db_column_validation_data_type,_db_column_form_data_type,_db_mysql_database_type,_db_table_type,_db_relationship_type


import colemen_utilities.type_utils as _type
import colemen_utilities.dict_utils as _obj
import colemen_utilities.list_utils as _lu
import colemen_utilities.database_utils.MySQL.Column.column_utils as _u
import colemen_utilities.database_utils.MySQL.Relationship.Relationship as _rel
import colemen_utilities.console_utils as _con
_log = _con.log





@dataclass
class Column:
    name:str = None
    data:_db_column_sql_data_type = None
    validation:_db_column_validation_data_type = None
    form:_db_column_form_data_type = None
    _relationship:_db_relationship_type = None
    '''The relationship instance associated to this column, if one exists.'''

    def __init__(self,database:_db_mysql_database_type,table:_db_table_type,data=None) -> None:
        self.database = database
        self._dbm = self.database._dbm
        self.table = table
        # self.schema_name = db.name
        self._column_name:str = None
        '''The SQL name for this column'''

        self.data:_db_column_sql_data_type = self.sql_data(self)
        self.form:_db_column_form_data_type = self.form_data(self)
        self.validation:_db_column_validation_data_type = self.validation_data(self)

        # @Mstep [IF] if a data dicitonary was provided
        if isinstance(data,(dict)):
            sql_data = data
            # @Mstep [IF] if sql_data is in the dict, the data is from a cache file.
            if 'sql_data' in data:
                # @Mstep [] set sql_data to the dicitonary's value
                sql_data = data['sql_data']
            # @Mstep [] have the data instance populate from the sql_data
            self.data.populate_from_meta(sql_data)

            if 'form_data' in data:
                self.form.populate_from_dict(data['form_data'])
            if 'validation' in data:
                self.validation.populate_from_dict(data['validation'])

        # @Mstep [] register this column with the database.
        self.database.register(self)



    @property
    def summary(self):
        '''
            Get the summary property's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 11-29-2022 12:28:21
            `@memberOf`: __init__
            `@property`: summary
        '''
        value = {
            "form_data":self.form.summary(),
            "validation":self.validation.summary(),
            "sql_data":self.data.summary(),
        }

        return value


    def _populate_from_meta_dictionary(self,data):
        # formatted = {}
        for k,v in data.items():
            k = k.lower()
            # formatted[k] = v
            if k == "data_type":
                self.py_data_type = v

            if k == "column_name":
                if v == "hash_id":
                    self.is_hash_id = True
            if k == "column_key":
                if "UNI" in v:
                    self.is_unique = True
                if "PRI" in v:
                    self.is_primary = True
            if k == "column_comment":
                self.description = v
            if k == "extra":
                if "auto_increment" in v:
                    self.auto_increment = True

            # if k == "character_maximum_length":
            #     self.validation.max_length = v

            if hasattr(self.data,k):
                setattr(self.data,k,v)

            if hasattr(self.validation,k):
                setattr(self.validation,k,v)

            if hasattr(self.form,k):
                setattr(self.form,k,v)


        # self.update_props_from_dict(formatted)

    # def validate(self,value):
    #     vtype = type(value).__name__
    #     if self.data[]


    @property
    def validation_schema(self):
        '''
            Get this Column's validation_schema

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-02-2022 17:25:19
            `@memberOf`: Column
            `@property`: validation_schema
        '''
        value = {
            "maxlength":self.validation.max_length,
        }
        return value

    # @property
    # def relationship(self)->_db_relationship_type:
    #     '''
    #         Get this Column's relationship instance, if it has one.

    #         `default`:None

    #         Meta
    #         ----------
    #         `@author`: Colemen Atwood
    #         `@created`: 12-16-2022 11:05:43
    #         `@memberOf`: Column
    #         `@property`: relationship
    #     '''
    #     value = self._relationship
    #     if value is None:
    #         if self.data.is_foreign_key is True:
    #             _log("Column.relationship --- Relationship Found","magenta")
    #             value = _rel.Relationship(
    #                 self.database,
    #                 self.table,
    #                 self,
    #                 self.data.foreign_key_data
    #             )
    #             self._relationship = value
    #     return value

    @dataclass
    class sql_data:
        _column:_db_column_type = None
        _column_comment:str = None
        _is_nullable:str = None
        auto_increment:bool = False
        '''True if this column auto_increments its own value.'''
        character_maximum_length:str = None
        '''The maximum number of characters allowed in this column'''
        character_octet_length:int = None
        character_set_name:str = None
        collation_name:str = None
        column_default:str = None
        '''The default value set to this column if no data is provided.'''
        column_key:str = None
        column_name:str = None
        '''The name of this column in the table.'''
        column_type:str = None
        data_type:str = None
        datetime_precision:str = None
        description:str = None
        extra:str = None
        generation_expression:str = None
        hash_id_prefix:str = None
        is_fulltext_indexed:bool = False
        '''True if this column has a fulltext index.'''
        is_timestamp:bool = False
        '''True if this column's name is "timestamp", meaning its used for tracking when the row was created.'''
        is_modified_timestamp:bool = False
        '''True if this column's name is "timestamp", meaning its used for tracking when the row was last modified.'''
        is_deleted:bool = False
        '''True if this column's name is "deleted", meaning its used for soft deletion of rows..'''
        is_hash_id:bool = False
        '''True if this column is a hash_id'''
        is_primary:bool = False
        '''True if this column is the primary key'''
        is_unique:bool = False
        '''True if this column has a unique constraint'''
        numeric_precision:str = None
        numeric_scale:str = None
        ordinal_position:int = None
        privileges:str = None


        constraint = None
        _is_foreign_key:bool = None
        '''True if this column has a foreign key constraint to another table.'''
        foreign_table_name:str = None
        '''The name of the foreign_table that this column references'''
        foreign_table_schema:str = None
        '''The name of the foreign table's schema that this column references'''
        foreign_column_name:str = None
        '''The name of the foreign column that this column references'''
        foreign_key_constraint_name:str = None
        '''The name of the foreign key constraint'''

        py_data_type:str = None
        '''The SQL data type converted to its python equivalent'''
        row_meta_col:bool = False
        '''True if this column is for internal use.'''

        _is_hash_id:bool = False


        def __init__(self,column:_db_column_type):
            self._column:_db_column_type = column

        def summary(self):
            value = {
                "auto_increment":self.auto_increment,
                "character_maximum_length":self.character_maximum_length,
                "character_octet_length":self.character_octet_length,
                "character_set_name":self.character_set_name,
                "collation_name":self.collation_name,
                # "column_comment":self._column_comment,
                "column_default":self.column_default,
                "column_key":self.column_key,
                "column_name":self.column_name,
                "column_type":self.column_type,
                "data_type":self.data_type,
                "datetime_precision":self.datetime_precision,
                "description":self.description,
                "extra":self.extra,
                "generation_expression":self.generation_expression,
                "hash_id_prefix":self.hash_id_prefix,
                "is_fulltext_indexed":self.is_fulltext_indexed,
                "is_hash_id":self.is_hash_id,
                "is_nullable":self.is_nullable,
                "is_primary":self.is_primary,
                "is_unique":self.is_unique,
                "is_modified_timestamp":self.is_modified_timestamp,
                "is_timestamp":self.is_timestamp,
                "is_deleted":self.is_deleted,
                "numeric_precision":self.numeric_precision,
                "numeric_scale":self.numeric_scale,
                "ordinal_position":self.ordinal_position,
                "privileges":self.privileges,
                "py_data_type":self.py_data_type,
                "row_meta_col":self.row_meta_col,
                "constraint":self.constraint,
                "is_foreign_key":self.is_foreign_key,
                "foreign_table_schema":self.foreign_table_schema,
                "foreign_table_name":self.foreign_table_name,
                "foreign_column_name":self.foreign_column_name,
                "foreign_key_constraint_name":self.foreign_key_constraint_name,
            }
            return value

        def populate_from_meta(self,data:dict):
            for k,v in data.items():
                k = k.lower()
                if k == "data_type":
                    self.py_data_type = _u.sql_type_to_python_type(v)

                if k == "constraint":
                    if isinstance(k,(dict)):
                        self.constraint = _obj.keys_to_snake_case(v)
                        if self.is_foreign_key:
                            self.foreign_table_schema = self.constraint['REFERENCED_TABLE_SCHEMA']
                            self.foreign_table_name = self.constraint['REFERENCED_TABLE_NAME']
                            self.foreign_column_name = self.constraint['REFERENCED_COLUMN_NAME']
                            self.foreign_key_constraint_name = self.constraint['CONSTRAINT_NAME']
                            if self._column.table.get_relationship(self.foreign_key_constraint_name) is None:
                                self._column._relationship = _rel.Relationship(
                                    self._column.database,
                                    name=self.constraint['CONSTRAINT_NAME'],
                                    foreign_table_schema = self.constraint['REFERENCED_TABLE_SCHEMA'],
                                    foreign_table_name = self.constraint['REFERENCED_TABLE_NAME'],
                                    foreign_column_name = self.constraint['REFERENCED_COLUMN_NAME'],
                                )
                    # self.is_foreign_key = True



                if k == "column_name":
                    self._column.name = v
                    if v == "modified_timestamp":
                        self.is_modified_timestamp = True
                    if v == "timestamp":
                        self.is_timestamp = True
                    if v == "deleted":
                        self.is_deleted = True
                    if v == "hash_id":
                        self.is_hash_id = True

                if k == "column_key":
                    if "UNI" in v:
                        self.is_unique = True
                    if "PRI" in v:
                        self.is_primary = True

                # if k == "column_comment":
                #     self._column_comment = v

                if k == "extra":
                    if "auto_increment" in v:
                        self.auto_increment = True




                if hasattr(self,k):
                    setattr(self,k,v)

                if hasattr(self._column.form,k):
                    print(f"form prop match found {k}")
                    setattr(self._column.form,k,v)
                
                if "validation_" in k:
                    k = k.replace("validation_","")
                    if k == "email":
                        k = "is_email"
                    if k == "unix_timestamp":
                        k = "is_timestamp"
                if hasattr(self._column.validation,k):
                    setattr(self._column.validation,k,v)


            if isinstance(self._column.table.raw_fulltext_indexes,(list)):
                for ft in self._column.table.raw_fulltext_indexes:
                    if ft['column_name'] == self.column_name:
                        self.is_fulltext_indexed = True


        @property
        def is_nullable(self)->bool:
            '''
                True if this column is allowed to be set to null

                `default`:False


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 11-29-2022 13:57:31
                `@memberOf`: PostArg
                `@property`: is_nullable
            '''
            value = self._is_nullable
            return value

        @is_nullable.setter
        def is_nullable(self,value:bool):
            '''
                Set the is_nullable value.

                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 11-29-2022 13:57:31
                `@memberOf`: PostArg
                `@property`: is_nullable
            '''

            self._is_nullable = _type.to_bool(value)


        @property
        def column_comment(self)->str:
            '''
                Get the column_comment value.

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 11-29-2022 14:37:31
                `@memberOf`: PostArg
                `@property`: column_comment
            '''
            value = self._column_comment
            return value

        @column_comment.setter
        def column_comment(self,value:str):
            '''
                Set the column_comment value.

                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 11-29-2022 14:37:31
                `@memberOf`: PostArg
                `@property`: column_comment
            '''
            self._column_comment = value
            yd = _u.parse_comment_yaml(value)
            if isinstance(yd,(dict)):
                # print(yd)
                for k,v in yd.items():
                    if hasattr(self,k):
                        setattr(self,k,v)

                    if hasattr(self._column.form,k):
                        setattr(self._column.form,k,v)

                    if hasattr(self._column.validation,k):
                        setattr(self._column.validation,k,v)

                    if k == "bool_opt":
                        setattr(self._column.validation,"is_boolean",True)

                    if k == "read_sus":
                        if v is True:
                            setattr(self._column.form,"read_form",True)


        @property
        def is_foreign_key(self):
            '''
                Get this SQLData's is_foreign_key

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-05-2022 12:52:11
                `@memberOf`: SQLData
                `@property`: is_foreign_key
            '''
            if self._is_foreign_key is None:
                if self.constraint is not None:
                    if 'REFERENCED_TABLE_NAME' in self.constraint:
                        self._is_foreign_key = True
                        self.foreign_table_schema = self.constraint['REFERENCED_TABLE_SCHEMA']
                        self.foreign_table_name = self.constraint['REFERENCED_TABLE_NAME']
                        self.foreign_column_name = self.constraint['REFERENCED_COLUMN_NAME']
                        self.foreign_key_constraint_name = self.constraint['CONSTRAINT_NAME']
                else:
                    self._is_foreign_key = False
            return self._is_foreign_key

        @is_foreign_key.setter
        def is_foreign_key(self,value):
            '''
                Set the SQLData's is_foreign_key property

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-05-2022 13:13:06
                `@memberOf`: SQLData
                `@property`: is_foreign_key
            '''
            self._is_foreign_key = value

        @property
        def foreign_key_data(self):
            '''
                Get this Column's foreign_key_data
                If this column is a foreign key, this will return a dictionary of the foreign key data:

                - schema_name
                - table_name
                - column_name
                - foreign_table_schema
                - foreign_table_name
                - foreign_column_name
                - foreign_key_constraint_name

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-16-2022 11:08:08
                `@memberOf`: Column
                `@property`: foreign_key_data
            '''
            value = {
                "schema_name":self._column.database.name,
                "table_name":self._column.table.table_name,
                "column_name":self.column_name,
                "foreign_table_schema":self.foreign_table_schema,
                "foreign_table_name":self.foreign_table_name,
                "foreign_column_name":self.foreign_column_name,
                "foreign_key_constraint_name":self.foreign_key_constraint_name,
            }
            return value

        @property
        def default(self):
            '''
                Get this Column's default

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-09-2022 13:31:56
                `@memberOf`: Column
                `@property`: default
            '''
            value = self.column_default
            if self.py_data_type == "boolean":
                from colemen_utilities.type_utils import bool_to_int
                value = bool_to_int(value)
                self.column_default = value
            return value

        @default.setter
        def default(self,value):
            '''
                Set the Column's default property

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-20-2022 14:02:01
                `@memberOf`: Column
                `@property`: default
            '''
            self.column_default = value

        @property
        def flask_url_placeholder(self):
            '''
                Get this Column's flask_url_placeholder
                
                <{type}:{column_name}>

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-21-2022 08:32:10
                `@memberOf`: Column
                `@property`: flask_url_placeholder
            '''
            name = self.column_name
            if self.is_hash_id is True:
                name = self._column.table.primary_column_name
            value = f"<{self.py_data_type}:{name}>"
            return value

        # @property
        # def is_hash_id(self):
        #     '''
        #         Get this Column's is_hash_id

        #         `default`:None


        #         Meta
        #         ----------
        #         `@author`: Colemen Atwood
        #         `@created`: 12-12-2022 11:51:24
        #         `@memberOf`: Column
        #         `@property`: is_hash_id
        #     '''
        #     result =  True if self.column_name.lower() in ["hash_id"] else False
        #     if result:
        #         print(f"column.is_hash_id")
        #     return result


        # @is_hash_id.setter
        # def is_hash_id(self,value:bool):
        #     '''
        #         Set the Column's is_hash_id property

        #         `default`:None


        #         Meta
        #         ----------
        #         `@author`: Colemen Atwood
        #         `@created`: 12-12-2022 11:53:51
        #         `@memberOf`: Column
        #         `@property`: is_hash_id
        #     '''
        #     self._is_hash_id = value

    @dataclass
    class validation_data:
        _column:_db_column_type = None
        default_on_failure:any = None
        force_integer:bool = False
        force_snake_case:bool = False
        max_length:int = None
        max_value:int = None
        min_length:int = None
        min_value:int = None
        no_purify:bool = False
        numeric_only:bool = False
        optional:bool = False
        _is_boolean:bool = False
        is_email:bool = False
        phone_number:bool = False
        # py_data_type:str = None
        required:bool = False
        unix_timestamp:bool = False
        value_options = None


        # ------------------------------ CREATE OPTIONS ------------------------------ #
        create_post_args:bool = False
        '''True if this column can be provided as a post argument in a create operation'''

        create_post_arg_required:bool = False
        '''True if this column is a required post argument to perform a create operation '''



        # ------------------------------ READ OPTIONS ------------------------------ #
        read_post_args:bool = True
        '''True if the this column can be searched for (allowed to be a where clause value)'''



        # ------------------------------ UPDATE OPTIONS ------------------------------ #
        update_post_args:bool = False
        '''True if this column is allowed to be referenced in a post argument for an update operation'''

        update_allow_change:bool = False
        '''True if this column's value is allowed to be updated'''



        # ------------------------------ DELETE OPTIONS ------------------------------ #
        delete_post_args:bool = False




        def __init__(self,column:_db_column_type):
            self._column:_db_column_type = column
            self._data:_db_column_sql_data_type = self._column.data
            # self._create_validation_schema = None



        def summary(self):
            value = {
                "default_on_failure":self.default_on_failure,
                "force_integer":self.force_integer,
                "force_snake_case":self.force_snake_case,
                "is_boolean":self.is_boolean,
                "is_email":self.is_email,
                "max_length":self._column.data.character_maximum_length,
                "max_value":self.max_value,
                "min_length":self.min_length,
                "min_value":self.min_value,
                "no_purify":self.no_purify,
                "numeric_only":self.numeric_only,
                "optional":self.optional,
                "phone_number":self.phone_number,
                "py_data_type":self._column.data.py_data_type,
                "required":self.required,
                "unix_timestamp":self.unix_timestamp,
                "value_options":self._column.form.value_options,
                "create_validation_schema":self.cerberus_schema("create",True),
                "read_validation_schema":self.cerberus_schema("read",True),
                "update_validation_schema":self.cerberus_schema("update",True),
                "delete_validation_schema":self.cerberus_schema("delete",True),
                "create_post_args":self.create_post_args,
                "read_post_args":self.read_post_args,
                "update_post_args":self.update_post_args,
                "update_allow_change":self.update_allow_change,
                "delete_post_args":self.delete_post_args,
            }
            return value

        def populate_from_dict(self,data:dict):
            for k,v in data.items():
                if hasattr(self,k):
                    setattr(self,k,v)

        @property
        def is_boolean(self)->bool:
            '''
                Get the is_boolean value.

                `default`:False


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 11-29-2022 14:32:57
                `@memberOf`: PostArg
                `@property`: is_boolean
            '''
            value = self._is_boolean
            if value is None:
                value = True if self._data.py_data_type =="boolean" else False
                self._is_boolean = value

            return value

        @is_boolean.setter
        def is_boolean(self,value:bool):
            '''
                Set the is_boolean value.

                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 11-29-2022 14:32:57
                `@memberOf`: PostArg
                `@property`: is_boolean
            '''
            self._is_boolean = value

        @property
        def py_data_type(self):
            '''
                Get this Column's py_data_type

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-09-2022 13:50:19
                `@memberOf`: Column
                `@property`: py_data_type
            '''
            value = self._data.py_data_type
            return value

        @py_data_type.setter
        def py_data_type(self,value):
            '''
                Set the Column's py_data_type property

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-12-2022 14:50:20
                `@memberOf`: Column
                `@property`: py_data_type
            '''
            pass
        # def create_validation_schema(self):
        #     '''
        #         Get this Column's create_validation_schema

        #         `default`:None


        #         Meta
        #         ----------
        #         `@author`: Colemen Atwood
        #         `@created`: 12-12-2022 14:09:02
        #         `@memberOf`: Column
        #         `@property`: create_validation_schema
        #     '''
        #     value = self.cerberus_schema("create")
        #     return value


        # @property
        def cerberus_schema(self,crud:str=None,force_function_names=False):
            ignore_form_setting = False
            value = {}

            if self._data.character_maximum_length is not None:
                value['maxlength'] = self._data.character_maximum_length

            if self.min_length is not None:
                value['minlength'] = self.min_length

            if self.value_options is not None:
                value['allowed'] = self.value_options

            if self._data.py_data_type is not None:
                value['type'] = self._data.py_data_type

            if self.is_boolean is True:
                value['type'] = "boolean"
                from colemen_utilities.type_utils import to_bool
                value['coerce'] = to_bool
                if force_function_names is True:
                    value['coerce'] = to_bool.__name__

            if self._data.column_name == "ip_address":
                from colemen_utilities.validate_utils.cerberus import ip_address
                value['check_with'] = ip_address
                if force_function_names is True:
                    value['check_with'] = ip_address.__name__

            if self._data.column_name == "email":
                from colemen_utilities.validate_utils.cerberus import is_email
                value['check_with'] = is_email
                if force_function_names is True:
                    value['check_with'] = is_email.__name__

            if self._data.is_hash_id:
                if isinstance(self._data.hash_id_prefix,(str)):
                    max_nonce = self._data.character_maximum_length - len(self._data.hash_id_prefix)
                    value['regex'] = f'{self._data.hash_id_prefix}_[a-zA-Z0-9]{{1,{max_nonce}}}'



            value['nullable'] = self._data.is_nullable
            if self._data.is_nullable is False:
                value['empty'] = False
            else:
                value['default'] = self._data.default



            # if self._data.is_timestamp:
            #     from colemen_utilities.validate_utils.cerberus import past_unix
            #     from colemen_utilities.validate_utils.cerberus import coerce_current_timestamp
            #     value['coerce'] = coerce_current_timestamp
            #     value['type'] = "integer"
            #     value['check_with'] = past_unix
            #     value['nullable'] = False
            #     value['empty'] = False
            #     if force_function_names is True:
            #         value['check_with'] = past_unix.__name__
            #         value['coerce'] = coerce_current_timestamp.__name__
            #     ignore_form_setting = True


            if ignore_form_setting is False:
                if crud == "create":
                    if self._column.form.create_form is False:
                        return None
                    if self._column.form.no_create is True:
                        return None
                if crud == "read":
                    if self._column.form.read_form is False:
                        return None
                if crud == "update":
                    if self._column.form.update_form is False:
                        return None
                    if self._column.form.no_update is True:
                        return None
                if crud == "delete":
                    if self._column.form.delete_form is False:
                        return None



            return value

        @property
        def allowed_in_create(self):
            '''
                Get this Column's allowed_in_create

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-13-2022 14:40:33
                `@memberOf`: Column
                `@property`: allowed_in_create
            '''
            allowed = True
            if self.no_create_post_args is True:
                allowed = False
            if self._column.form.create_form is False:
                allowed = False
            if self._column.form.no_create is True:
                allowed = False
            return allowed



    @dataclass
    class form_data:
        _column:_db_column_type = None
        data:_db_column_sql_data_type = None

        no_post_args:bool = False
        '''True if this column should never be allowed as a form body key'''

        no_form:bool = False
        '''True if this column should not be included in any form.'''

        create_form:bool = False
        '''True if this column should be included in create forms'''
        read_form:bool = True
        '''True if this column should be included in read forms'''
        update_form:bool = False
        '''True if this column should be included in update forms'''
        delete_form:bool = False
        '''True if this column should be included in delete forms'''

        _input_type:str = None
        '''The type of input used to enter the data.'''

        no_create:bool = False
        '''True if this column should not be included in any create form.'''
        no_read:bool = False
        '''True if this column should not be included in any read form.'''
        no_update:bool = False
        '''True if this column should not be included in any update form.'''
        no_delete:bool = False
        '''True if this column should not be included in any delete form.'''

        _value_options = None
        '''A list of values used as options in a radio input.'''

        def __init__(self,column:_db_column_type):
            self._column:_db_column_type = column
            self.data:_db_column_sql_data_type = column.data
            self.create_forms = []
            self.read_forms = []
            self.update_forms = []
            self.delete_forms = []

        def summary(self):
            value = {
                "create_form":self.create_form,
                "read_form":self.read_form,
                "update_form":self.update_form,
                "delete_form":self.delete_form,
                "input_type":self.input_type,
                "no_form":self.no_form,
                "no_create":self.no_create,
                "no_read":self.no_read,
                "no_update":self.no_update,
                "no_delete":self.no_delete,
                "value_options":self.value_options,
                "no_post_args":self.no_post_args,
                "create_forms":self.create_forms,
                "read_forms":self.read_forms,
                "update_forms":self.update_forms,
                "delete_forms":self.delete_forms,
            }
            # output = {}
            # for k,v in value.items():
            #     if v is False:
            #         continue
            #     output[k] = v
            return value

        def populate_from_dict(self,data:dict):
            for k,v in data.items():
                if k == "create_form":
                    self.create_form = True
                    if isinstance(v,(list,str)):
                        self.add_form('create',v)

                if k == "read_form":
                    self.read_form = True
                    if isinstance(v,(list,str)):
                        self.add_form('read',v)

                if k == "update_form":
                    self.update_form = True
                    if isinstance(v,(list,str)):
                        self.add_form('update',v)

                if k == "delete_form":
                    self.delete_form = True
                    if isinstance(v,(list,str)):
                        self.add_form('delete',v)

                if self.create_form is True and self.no_update is False:
                    self.update_form = True

                if self._column.data.is_hash_id is True or self._column.data.is_primary is True:
                    self.delete_form = True
                    self.no_delete = False
                    self.no_post_args = False

                if hasattr(self,k):
                    setattr(self,k,v)
                else:
                    _log(f"No column form attribute for {k}:{v}","warning")

        def add_form(self,crud_type:str,form_name):
            crud_type = crud_type.lower()
            if crud_type not in ['create','read','update','delete']:
                return False
            form_names = _lu.force_list(form_name)
            for form_name in form_names:
                if crud_type == 'create':
                    if form_name not in self.create_forms:
                        self.create_forms.append(form_name)
                if crud_type == 'read':
                    if form_name not in self.read_forms:
                        self.read_forms.append(form_name)
                if crud_type == 'update':
                    if form_name not in self.update_forms:
                        self.update_forms.append(form_name)
                if crud_type == 'delete':
                    if form_name not in self.delete_forms:
                        self.delete_forms.append(form_name)

        @property
        def input_type(self):
            '''
                The type of input used to enter the data.

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-19-2022 11:57:41
                `@memberOf`: Column
                `@property`: input_type
            '''
            if self._input_type is None or self._input_type is False:
                if self._column.data.py_data_type in ['string']:
                    if self._column.data.character_maximum_length < 256:
                        self._input_type = "single_line_input"

                    if self._column.data.character_maximum_length > 256:
                        self._input_type = "text_area_input"

                if self._column.data.py_data_type == "integer":
                    self._input_type = "number_input"

                if self._column.data.py_data_type == "boolean":
                    self._input_type = "toggle_button"


                if self._column.validation.unix_timestamp is True and self._column.data.py_data_type in ['integer']:
                    self._input_type = "date_input"

                if self._column.data.column_name in ["timestamp","modified_timestamp","start_timestamp","end_timestamp","deleted","birthday","deactivated","established","last_login_timestamp","last_activity_timestamp","email_verified","disabled","is_abandoned","last_abandoned_alert"]:
                    self._input_type = "date_input"

                if self.value_options is not None:
                    self._input_type = "select_input"


            return self._input_type

        @input_type.setter
        def input_type(self,value):
            '''
                Set the Column's input_type property

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-19-2022 12:03:28
                `@memberOf`: Column
                `@property`: input_type
            '''
            self._input_type = value


        @property
        def value_options(self)->list:
            '''
                A list of values used as options in a select input.

                `default`:None


                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-19-2022 12:16:17
                `@memberOf`: PostArg
                `@property`: value_options
            '''
            return self._value_options

        @value_options.setter
        def value_options(self,value):
            '''
                Set the value_options value.

                Meta
                ----------
                `@author`: Colemen Atwood
                `@created`: 12-19-2022 12:16:17
                `@memberOf`: PostArg
                `@property`: value_options
            '''
            if isinstance(value,(bool)) is True or value is None:
                return False
            self._value_options = value


# def _format_cerberus_schema_for_json(schema):
#     cerb = {}
#     if schema is not None:
#         data = {}
#         for k,v in schema.items():
#             if k in ["check_with",'coerce']:
#                 v = v.__name__
#             data[k] = v
#         # cerb[x.name] = data
#         return data

