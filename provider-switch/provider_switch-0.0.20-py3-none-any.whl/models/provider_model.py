from datetime import datetime

from provider_switch.exceptions import ResponseNotFoundException, ValidationResponseException
from provider_switch.helpers.common_helper import CommonHelper
from provider_switch.helpers.dotdictify import dotdictify
from provider_switch.ssm.ssm_client import SSMClient


class ProviderModel(object):
    _excludes = ['_format_values', 'ssm_client', 'status', 'url', 'headers', 'request', 'response',
                 'retry_when_not_found']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.social_type = kwargs.get('social_type', None)
        self.api_key = kwargs.get('api_key', None)
        self.die_count = kwargs.get('die_count', 0)
        self.success_count = kwargs.get('success_count', 0)
        self.status = kwargs.get('status', True)
        self.config = kwargs.get('config', {})
        self.priority = kwargs.get('priority', 0)

        self.is_over_quota = kwargs.get('is_over_quota', False)
        self.quotas = kwargs.get('quotas', 1000)
        self.current_usage_quotas = kwargs.get('current_usage_quotas', 0)
        self.quota_refresh_time = kwargs.get('quota_refresh_time', datetime.now().timestamp())

        self.session_fail = 0
        self.session_success = 0
        self.retry_delay = kwargs.get('retry_delay', 2)
        self.retry_when_not_found = kwargs.get('retry_when_not_found', False)
        self.retry_time = kwargs.get('retry_time', 1)
        self.timeout = kwargs.get('timeout', 30)

        self.request = kwargs.get('request', {})
        self.response = kwargs.get('response', {})

        self._format_values = dict(api_name=self.name, api_key=self.api_key)

        self.ssm_client = SSMClient()

        headers = self.get_attr('config.default_headers')
        spec_headers = self.get_attr('request.specs.headers')
        headers.update(spec_headers) if spec_headers else headers

        path = self.get_attr('request.specs.path')

        if 'https://' not in path:
            path = "https://{api_name}.p.rapidapi.com" + path

        self.url = CommonHelper.format_data(path, self._format_values)
        self.headers = CommonHelper.format_data(headers, self._format_values)

    def _validation(self, format, data, is_reverse=True):  # noqa: C901
        format_keys = format.keys()
        data_dict = dotdictify(data)

        for key in format_keys:
            try:
                value = getattr(data_dict, key)
            except Exception:
                if is_reverse is True:
                    raise Exception('Key not found: {}'.format(key))
                else:
                    return True

            format_value = format.get(key, None)

            if type(format_value) == bool:

                if is_reverse is True:
                    if value != format_value:
                        raise ValidationResponseException(key=key)
                else:
                    if value == format_value:
                        raise ResponseNotFoundException(key=key)

            elif type(format_value) == str:

                if is_reverse is True:
                    if format_value == '' and value is None:
                        raise ValidationResponseException(key=key)
                else:
                    if format_value == value:
                        raise ResponseNotFoundException(key=key)

                if format_value.__contains__('contain(\''):
                    format_value = format_value.replace('contain(\'', '').replace('\')', '')

                    if is_reverse is True:
                        if format_value not in value:
                            raise ValidationResponseException(key=key)
                    else:
                        if format_value in value:
                            raise ResponseNotFoundException(key=key)

    def check_response(self, response):
        try:
            format = self.response.get('format', None)
            success_format = format.get('success', None)
            not_found_format = format.get('not_found', None)

            if not success_format or not not_found_format:
                return {
                    "status": True,
                    "retry": False,
                }

            if not_found_format:
                self._validation(not_found_format, response, False)

            if success_format:
                self._validation(success_format, response)

            return {
                "status": True,
                "retry": False,
            }
        except ValidationResponseException:
            return {
                "status": False,
                "retry": True,
            }
        except ResponseNotFoundException:
            if self.retry_when_not_found:
                return {
                    "status": False,
                    "retry": True,
                }
            return {
                "status": False,
                "retry": False,
            }

    def get_attr(self, key) -> str:
        try:
            if not key:
                return None

            dicts = dotdictify(self.__dict__)
            return getattr(dicts, key)
        except Exception:
            return None

    def is_good(self):
        return self.status is True and self.is_over_quota is False

    def increment_session_fail(self):
        self.session_fail += 1

    def increment_session_success(self):
        self.session_success += 1

    def refresh_session_fail(self):
        self.session_fail = 0

    def set_inactive(self):
        self.status = False
        # self.ssm_client.set_providers(self.to_json())
        pass

    def set_active(self):
        self.status = True

    def sync(self, provider_data):
        self.ssm_client.set_providers(provider={**self.to_json(), **provider_data})

    def to_json(self):
        self_dict = self.__dict__
        self_dict_keys = self_dict.keys()
        json_data = {}

        for key in self_dict_keys:
            if key not in self._excludes:
                json_data[key] = self_dict.get(key)

        return json_data
