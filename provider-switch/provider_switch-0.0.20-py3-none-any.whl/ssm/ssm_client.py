from json import dumps, loads

import boto3


class SSMClient(object):

    def __init__(self) -> None:
        self.client: boto3.client = boto3.client("ssm")

    def get_providers(self, social_type):
        providers = self._get_parameter_by_path(name='/rapid_api_providers' + "/" + social_type)
        sorted_providers = sorted(providers, key=lambda x: x['priority'], reverse=False)
        enabled_providers = list(filter(lambda x: x['status'] is True, sorted_providers))
        return enabled_providers

    def set_providers(self, provider):
        parameter_name = '/rapid_api_providers' + "/" + \
                         provider.get('social_type', None) + "/" + provider.get('name', None) + "-" + provider.get('id',
                                                                                                                   None)
        parameter = self._get_parameter(name=parameter_name)

        if not parameter:
            return

        parameter_keys = list(provider.keys())

        for key in parameter_keys:
            val = provider.get(key, None)
            if val is not None:
                parameter[key] = val

        if provider and parameter:
            if parameter['quotas_remaining'] == 0:
                parameter['is_over_quota'] = True

            parameter['die_count'] = parameter['die_count'] + provider.get('session_fail', 0)
            parameter['success_count'] = parameter['success_count'] + provider.get('session_success', 0)

        return self._set_parameter(
            name=parameter_name,
            value=dumps(parameter),
        )

    def _get_parameter(self, name, with_decryption=True):
        parameter_raw = self.client.get_parameter(
            Name=name,
            WithDecryption=with_decryption,
        )

        return loads(parameter_raw['Parameter']['Value'])

    def _get_parameter_by_path(self, name, with_decryption=True):
        parameter_raw = self.client.get_parameters_by_path(
            Path=name,
            Recursive=True,
            WithDecryption=with_decryption,
        )

        parameters = parameter_raw['Parameters']
        return list(map(lambda x: loads(x['Value']), parameters))

    def _set_parameter(self, name, value, type='String', overwrite=True):
        return self.client.put_parameter(
            Name=name,
            Value=value,
            Type=type,
            Overwrite=overwrite,
        )

    def get_template(self, path):
        template = self._get_parameter(name=path)
        return template