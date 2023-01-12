import re
from .dotdictify import dotdictify


class MappingData(object):

    def __init__(self) -> None:
        pass

    def map(self, input: dict = None, template: dict = None) -> dict:
        input = input if input else self.input
        template = template if template else self.template

        if not input or not template:
            raise Exception('Input or template is not provided')

        mapped_data = {}
        if template:
            mapped_data = self._map_response(input, template)

        return {
            **input,
            **mapped_data
        }

    def _map_list(self, data: list, key: str) -> list:
        values = self.map(template=key, input=data)
        return values

    def _map_response(self, input: dict, template: dict) -> dict:  # noqa: C901
        mapped_data = {}
        input_vdict = dotdictify(input)
        regex = "\[.+?\]"  # noqa: W605

        for key, value in template.items():
            try:
                val_key = value
                map_key = key

                if type(value) is list:
                    val_key = '.'.join(value)

                if type(key) is str and re.search(regex, key):
                    key_raw = key.replace('[', '').replace(']', '')
                    keys = key_raw.split(':')
                    map_key = keys[0]
                    new_values = input_vdict.__getattr__(keys[1])
                    new_type = keys[2]

                    if new_type == 'list':
                        if type(new_values) is list:
                            data = []
                            for item in new_values:
                                data.append(self._map_list(item, val_key))

                            mapped_data[map_key] = data
                        else:
                            print('[Error] MappingData: ', keys[1], ' is not a list')
                    elif new_type == 'dict':
                        mapped_data[map_key] = self._map_list(new_values, val_key)
                    else:
                        continue
                elif type(key) is str and key == '*':
                    if ".*" in val_key:
                        temp_data = input_vdict.__getattr__(val_key.replace('.*', ''))
                    if val_key == "*":
                        temp_data = input_vdict
                    else:
                        temp_data = input_vdict.__getattr__(val_key)

                    mapped_data = {**mapped_data, **temp_data}
                    continue
                else:
                    if type(val_key) is str:
                        data = input_vdict.__getattr__(val_key)
                        mapped_data[map_key] = data
                    elif type(val_key) is dict:
                        mapped_data[map_key] = self._map_response(input, val_key)

            except Exception:
                # print('[Error] MappingData: ', e)
                continue

        try:
            make_response_data = dotdictify(mapped_data)
            return make_response_data
        except KeyError as e:
            print('[Error] MappingData: ', e)
            return {}
