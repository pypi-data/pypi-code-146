from provider_switch.helpers.mapping_data import MappingData
from provider_switch.models.provider_model import ProviderModel


class ResponseHelper(object):
    def __init__(self, provider: ProviderModel):
        self.provider = provider
        provider_response = provider.response if provider.response else {}
        self.mapping_data_fields = provider_response.get('mapping_data_fields', {})
        self.default_response = dict({
            "data": {},
            "paging": {},
            "message": "",
            "description": "",
        })

    def standardize_response(self, response: dict) -> dict:
        mapped_response = {}
        if self.mapping_data_fields:
            mapped_response = MappingData().map(template=self.mapping_data_fields, input=response)
        else:
            mapped_response = response

        return mapped_response
