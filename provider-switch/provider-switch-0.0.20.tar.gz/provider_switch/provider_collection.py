import os
from json import load

from .models.provider_model import ProviderModel
from .ssm.ssm_client import SSMClient
from .utils.common import Common


class ProviderCollection(object):
    def __init__(self, driver_type: str, **kwargs):
        self.providers = []
        self.driver_type = driver_type
        self.social_type = kwargs.get('social_type', None)
        self.service_name = kwargs.get('service_name', None)
        self.retry_when_not_found = kwargs.get('retry_when_not_found', False)
        self.ssm_client = SSMClient()
        self._prepare()

    def get_providers(self) -> list:
        """Get providers from SSM Parameter Store

        Returns:
            list: List of providers
        """
        return self.providers

    def _prepare(self):
        """Prepare to get providers

        Raises:
            Exception: can not get providers
        """
        providers = self.ssm_client.get_providers(self.social_type)

        if not providers:
            raise Exception('Can not get providers')

        self._get_providers_info(providers)

    def _get_providers_info(self, providers) -> None:
        """Get providers info from template file

        Args:
            providers (list): List of provider get from SSM Parameter Store

        Raises:
            Exception: Not found template file
        """
        if self.driver_type == 'json':
            self._load_providers_from_json(providers)
        if self.driver_type == 'ssm':
            self._load_providers_from_parameter_store(providers)

        if not self.providers:
            raise Exception('No provider found.')

    def _build_file_template_dir(self, provider_name: str) -> str:
        """Build file template dir from provider name

        Args:
            provider_name (str): Provider name

        Returns:
            str: File template dir
        """

        file_dir = f'{Common.get_project_root()}/core/templates/' \
                   f'{self.social_type}/third_party_api_constants/{provider_name}/{self.service_name}.json'

        if not os.path.exists(file_dir):
            print("------------------")
            print("- File dir: ", file_dir)
            print("- Provider name: ", provider_name)
            print("------------------")
            return False

        return file_dir

    def _load_providers_from_json(self, providers):
        """Load providers from json file

        Args:
            providers (list): list of providers get from SSM Parameter Store
        """
        for provider in providers:
            provider_name = provider.get('name', None)
            if not provider_name:
                continue

            provider_name = provider_name.lower().replace('-', '_')
            file_dir = self._build_file_template_dir(provider_name=provider_name)
            if not file_dir:
                continue

            with open(file_dir) as f:
                try:
                    provider_info = load(f)
                except ValueError:
                    print('Can not load provider info from json file {}'.format(file_dir))
                    continue

                request = provider_info.get('request', None)
                response = provider_info.get('response', None)
                provider_data = ProviderModel(
                    request=request,
                    response=response,
                    retry_when_not_found=self.retry_when_not_found,
                    **provider,
                )

                self.providers.append(provider_data)

    def _load_providers_from_parameter_store(self, providers):
        """Load providers from pramameter store
        Args:
            providers (list): list of providers get from SSM Parameter Store
        """
        for provider in providers:
            provider_name = provider.get('name', None)
            if not provider_name:
                continue

            provider_name = provider_name.lower()
            template_path = self.build_template_path_ssm(provider_name=provider_name)
            try:
                provider_info = self.ssm_client.get_template(template_path)
                if not provider_info:
                    raise Exception("Not found templates")
                # provider_info = loads(templates)
            except Exception:
                print('Can not load provider info from parameter store {}'.format(template_path))
                continue

            request = provider_info.get('request', None)
            response = provider_info.get('response', None)
            provider_data = ProviderModel(
                request=request,
                response=response,
                retry_when_not_found=self.retry_when_not_found,
                **provider,
            )
            self.providers.append(provider_data)

    def build_template_path_ssm(self, provider_name):
        return '/rapid_api_templates' + "/" + self.social_type + "/" + provider_name + "/" + self.service_name