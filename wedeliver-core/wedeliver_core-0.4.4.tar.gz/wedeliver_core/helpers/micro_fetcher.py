import flask_sqlalchemy

from wedeliver_core import WeDeliverCore
from wedeliver_core.helpers.exceptions import AppMicroFetcherError, AppFetchServiceDataError
import requests
import json

from wedeliver_core.helpers.get_obj_value import get_obj_value

from wedeliver_core.helpers.service_config import ServiceConfig

from wedeliver_core.helpers.enums import QueryTypes


class MicroFetcher(object):
    base_data = None
    app = None
    service_name = None
    service_url = None
    fields = None
    table_name = None
    column_name = None
    compair_operator = None
    column_values = None
    output_key = None
    lookup_key = None
    module_name = None
    function_params = None
    query_type = None
    search_list = None

    def __init__(self, service):
        self.app = WeDeliverCore.get_app()

        if isinstance(service, ServiceConfig):
            service = service.initialize()
            service_name = service.name
            service_url = service.url
        else:
            service_name = service
            service_url = None

        env_service_url = self.app.config.get(service_name)

        self.service_url = env_service_url if env_service_url else service_url

        self.service_name = service_name
        if not self.service_url:
            raise AppMicroFetcherError('Service {} not defined on Env or in ServiceConfig'.format(self.service_url))

    def join(self, base_data, output_key=None):
        self.base_data = base_data
        self.query_type = QueryTypes.SIMPLE_TABLE.value
        if output_key:
            output_key = output_key.split('as ')[1]

        self.output_key = "{}".format(self.service_name.split('_')[0].lower()) if not output_key else output_key
        return self

    def _prepare_search_list(self):
        output = dict()
        for index, item in enumerate(self.base_data):
            for search_column in self.search_configs.get("search_priority"):
                sanitize = None
                if isinstance(search_column, dict):
                    search_column_name = search_column.get('key')
                    operator = search_column.get('operator') or "IN"
                    sanitize = search_column.get('sanitize')
                else:
                    search_column_name = search_column
                    operator = 'IN'

                value = item.get(search_column_name)
                if sanitize and isinstance(sanitize, list):
                    for _san in sanitize:
                        value = _san(value)

                if value:
                    if not output.get(search_column_name):
                        output[search_column_name] = dict(
                            search_key=search_column_name,
                            operator=operator,
                            inputs=dict()
                        )
                    if not output[search_column_name]['inputs'].get(value):
                        output[search_column_name]['inputs'][value] = dict(
                            indexes=[index],
                            search_value=value
                        )
                    else:
                        output[search_column_name]['inputs'][value]["indexes"].append(index)
                    break

        output = list(output.values())
        for item in output:
            item['inputs'] = list(item['inputs'].values())

        self.search_list = output

    def search_config(self, configs):
        self.search_configs = configs
        self._prepare_search_list()
        return self

    def global_configs(self, **keywords):
        self.global_configs = keywords
        return self

    def feed_list(self, base_data, output_key=None):
        join_result = self.join(base_data, output_key)
        self.query_type = QueryTypes.SEARCH.value
        return join_result

    def select(self, *args):
        self.fields = list(args)
        return self

    def filter(self, *args):
        against = args[0].split('.')
        self.compair_operator = args[1]
        self.lookup_key = args[2]
        self.column_values = set()
        if isinstance(self.base_data, dict):
            self.column_values.add(get_obj_value(self.base_data, self.lookup_key))
        else:
            if isinstance(self.base_data, flask_sqlalchemy.Pagination):
                data = self.base_data.items
            else:
                data = self.base_data

            for row in data:
                self.column_values.add(get_obj_value(row, self.lookup_key))

        if not len(self.column_values):
            return self
            # raise AppMicroFetcherError('Lookup key {} not found'.format(self.lookup_key))

        self.column_values = list(filter(None, self.column_values))
        self.column_values = self.column_values[0] if len(self.column_values) == 1 else self.column_values

        if self.compair_operator not in ('=', 'IN'):
            raise AppMicroFetcherError('Only == currently supported')

        self.compair_operator = 'IN' if isinstance(self.column_values, list) else self.compair_operator

        self.table_name = against[0]
        self.column_name = against[1]

        self.fields.append(self.column_name)
        return self

    def fetch(self):
        if self.column_values or self.module_name or self.query_type == QueryTypes.SEARCH.value:
            return self._call_api()
        else:
            return self.base_data

    def with_params(self, **kwargs):
        self.function_params = kwargs
        return self

    def from_function(self, module_name):
        self.query_type = QueryTypes.FUNCTION.value
        self.module_name = module_name
        return self

    def _call_api(self):

        url = "{}/fetch_relational_data".format(self.service_url)

        payload_dict = dict()
        if self.query_type in [QueryTypes.SIMPLE_TABLE.value, QueryTypes.FUNCTION.value]:
            payload_dict.update(
                dict(
                    fields=self.fields,
                    table_name=self.table_name,
                    column_name=self.column_name,
                    compair_operator=self.compair_operator,
                    column_values=self.column_values,
                )
            )

            if self.query_type == QueryTypes.FUNCTION.value:
                payload_dict.update(
                    functions=[
                        dict(
                            name=self.module_name,
                            fields=self.fields,
                            params=self.function_params if self.function_params else dict()
                        )
                    ]
                )

        elif self.query_type == QueryTypes.SEARCH.value:
            payload_dict.update(dict(
                query_type=self.query_type,
                table_name=self.search_configs.get("table_name"),
                search_list=self.search_list,
                append_extra=self.search_configs.get("append_extra"),
                use_country_code=self._get_global_config(key="use_country_code", default_value=True),
            ))

        payload = json.dumps(payload_dict)
        headers = {
            'country_code': self._get_global_config(key="country_code", default_value="sa"),
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            self.app.logger.error(response.text)
            raise AppFetchServiceDataError()

        result = response.json()

        if self.base_data:
            return self._map_base(result)

        return result

    def _get_global_config(self, key, default_value):
        if hasattr(self, 'global_configs') and isinstance(self.global_configs, dict):
            if self.global_configs.get(key) is None:
                return default_value
            else:
                return self.global_configs.get(key)
        else:
            return default_value

    def _map_base(self, result):
        if self.query_type == QueryTypes.SEARCH.value:
            # map search result with the original object.
            _result = result.get("result")
            for item in _result:
                for _input in item.get('inputs'):
                    for _index in _input.get('indexes'):
                        self.base_data[_index][self.output_key] = _input.get('matched_id')
                        append_extra = self.search_configs.get('append_extra') if isinstance(self.search_configs,
                                                                                             dict) else []
                        for _ap_col in append_extra:
                            self.base_data[_index][_ap_col] = _input.get(_ap_col) if _input.get('matched_id') else \
                                self.base_data[_index].get(_ap_col)

            validation_result = []
            for _val in result.get("validation"):
                for _ind in _val.get("indexes"):
                    _val.pop("indexes", None)
                    validation_result.append(dict(
                        index=_ind,
                        **_val
                    ))
            return validation_result
        else:
            if isinstance(self.base_data, dict):
                if self.query_type == QueryTypes.SIMPLE_TABLE.value:
                    for rd in result:
                        if self.base_data.get(self.lookup_key) == rd.get(self.column_name):
                            try:
                                setattr(self.base_data, self.output_key, rd)
                            except AttributeError:
                                if self.base_data.get(self.output_key):
                                    if not isinstance(self.base_data[self.output_key], list):
                                        self.base_data[self.output_key] = [self.base_data[self.output_key]]

                                    self.base_data[self.output_key].append(
                                        rd
                                    )
                                else:
                                    self.base_data[self.output_key] = rd

                else:
                    for rd in result:
                        if self.base_data.get(self.lookup_key) == rd.get(self.column_name):
                            try:
                                setattr(self.base_data, self.output_key, rd)
                            except AttributeError:
                                self.base_data[self.output_key] = rd
            else:
                if isinstance(self.base_data, flask_sqlalchemy.Pagination):
                    data = self.base_data.items
                else:
                    data = self.base_data

                for row in data:
                    for rd in result:
                        if get_obj_value(row, self.lookup_key) == rd.get(self.column_name):
                            try:
                                setattr(row, self.output_key, rd)
                            except AttributeError:
                                row[self.output_key] = rd

                if isinstance(self.base_data, flask_sqlalchemy.Pagination):
                    self.base_data.items = data
                else:
                    self.base_data = data

            return self.base_data
