from wedeliver_core.helpers.sql import sql
import importlib
import os

from wedeliver_core.helpers.enums import QueryTypes
from wedeliver_core.helpers.search_function import search_function
from datetime import datetime,date

def fetch_relational_data(
        fields=None,
        table_name=None,
        column_name=None,
        compair_operator=None,
        column_values=None,
        functions=None,
        query_type=None,
        search_list=None,
        append_extra=None,
        use_country_code=None,

):
    # app = WeDeliverCore.get_app()
    # db = app.extensions['sqlalchemy'].db

    if query_type == QueryTypes.SEARCH.value:
        result, validation = search_function(table_name=table_name, search_list=search_list, append_extra=append_extra,
                                             use_country_code=use_country_code)
        return dict(
            result=result,
            validation=validation
        )
    else:
        relational_data_result = []

        if table_name:
            query = """
                SELECT {fields}
                FROM {table_name}
                WHERE {column_name} {compair_operator} {column_values}
                """.format(
                fields=', '.join(fields),
                table_name=table_name,
                column_name=column_name,
                compair_operator=compair_operator,
                column_values="('{}')".format(
                    "', '".join([str(val) for val in column_values])) if compair_operator == 'IN' else "'{}'".format(
                    column_values),
            )
            relational_data_result = sql(query)

        if functions and isinstance(functions, list):
            def _update_relational_data_result(function_result, fields):
                if relational_data_result:
                    for rd in relational_data_result:
                        for f in fields:
                            rd[f] = function_result.get(f) if isinstance(function_result,
                                                                         dict) else function_result.__dict__.get(f)
                else:
                    fields_dict = dict()
                    for f in fields:
                        fields_dict[f] = function_result.get(f) if isinstance(function_result,
                                                                              dict) else function_result.__dict__.get(f)
                    relational_data_result.append(fields_dict)

            for func in functions:
                function_file, function_call = os.path.splitext(func.get('name'))
                m = importlib.import_module(function_file)
                method = getattr(m, function_call[1:])

                function_result = method(**func.get('params'))

                fields = func.get('fields')
                if not fields:
                    relational_data_result = function_result
                elif function_result:
                    if isinstance(function_result, list):
                        for row in function_result:
                            _update_relational_data_result(row, fields)
                    else:
                        _update_relational_data_result(function_result, fields)
    # check if the result contain datetime, or date object and convert it to string
    for row in relational_data_result:
        for key, value in row.items():
            if isinstance(value, datetime):
                row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                row[key] = value.strftime('%Y-%m-%d')
    return relational_data_result
