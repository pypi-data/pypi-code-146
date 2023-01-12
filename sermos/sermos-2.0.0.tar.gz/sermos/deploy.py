""" Utilities for deploying applications to Sermos.

    Example CLI Usage::

        $ honcho run -e .env sermos deploy
        $ honcho run -e .env sermos status

    Example Programmatic Usage::

        from sermos.deploy import SermosDeploy

        sd = SermosDeploy(
            os.environ.get("SERMOS_DEPLOYMENT_ID")
            os.environ.get("SERMOS_ACCESS_KEY")
        )

        # To Invoke
        status = sd.invoke_deployment()
        print(status)

        # To Check Status:
        status = sd.get_deployment_status()
        print(status)

"""
import base64
import logging
import json

from sermos.sermos_yaml import load_sermos_config
from sermos.cloud import SermosCloud

logger = logging.getLogger(__name__)


class SermosDeploy(SermosCloud):
    """ Primary Sermos Deployment class for invocation and status updates.
    """
    def __init__(self,
                 access_key: str = None,
                 deployment_id: str = None,
                 sermos_yaml_filename: str = None,
                 base_url: str = None):
        """ Arguments:
                access_key (optional): Access key, issued by Sermos, that
                    dictates the environment into which this request will be
                    deployed. Defaults to checking the environment for
                    `SERMOS_ACCESS_KEY`. If not found, will exit.
                deployment_id (optional): UUID for Deployment. Find in your
                    Sermos Cloud Console.
                sermos_yaml_filename (optional): Relative path to find your
                    `sermos.yaml` configuration file. Defaults to `sermos.yaml`.
                base_url (optional): Defaults to primary Sermos Cloud base URL.
                    Only modify this if there is a specific, known reason to do so.
                    Can also set through environment `SERMOS_BASE_URL`.
        """
        super().__init__(access_key, deployment_id, base_url)
        self.sermos_yaml_filename = sermos_yaml_filename
        self.sermos_yaml = None  # Established later, only on `invoke`
        self.encoded_sermos_yaml = None  # Established later, only on `invoke`
        self.deploy_payload = None  # Established later, only on `invoke`

    def _set_encoded_sermos_yaml(self):
        """ Provide the b64 encoded sermos.yaml file as part of request.
            Primarily used to get the custom workers definitions, etc. so
            the deployment endpoint can generate the values.yaml.
        """
        self.sermos_yaml = load_sermos_config(self.sermos_yaml_filename,
                                              as_dict=False)
        self.encoded_sermos_yaml = base64.b64encode(
            self.sermos_yaml.encode('utf-8')).decode('utf-8')

    def _set_deploy_payload(self):
        """ Set the deployment payload correctly.
        """
        self._set_encoded_sermos_yaml()
        self.deploy_payload = {"sermos_yaml": self.encoded_sermos_yaml}

    def get_deployment_status(self):
        """ Info on a specific deployment
        """
        resp = self.get(self.services_url)
        services = resp.json().get('data', {}).get('results', [])
        status_map = {
            'data': {
                'results': []
            },
            'message': 'Status of all Deployment Services'
        }
        for service in services:
            status_map['data']['results'].append({
                'service_id':
                service['niceId'],
                'name':
                service['name'],
                'status':
                service['status']
            })
        return status_map

    def validate_deployment(self,
                            output_file: str = None,
                            output_format: str = 'yaml',
                            print_output: bool = False):
        """ Test rendering sermos.yaml and validate.
        """
        # Running this will raise an exception if something is invalid.
        self._set_deploy_payload()

        if output_file and output_format == 'yaml':
            with open(output_file, 'w') as f:
                f.write(self.sermos_yaml)

        if output_file and output_format == 'json':
            with open(output_file, 'w') as f:
                f.write(
                    json.dumps(load_sermos_config(self.sermos_yaml_filename)))

        if print_output:
            if output_format == 'yaml':
                print(self.sermos_yaml)
            elif output_format == 'json':
                print(load_sermos_config(self.sermos_yaml_filename))
            else:
                print(f"Unknown requested output format: {output_format}")

        return True

    def invoke_deployment(self):
        """ Invoke a Sermos AI Deployment
        """
        self._set_deploy_payload()

        # Make request to your environment's endpoint
        return self.post(self.deploy_url, self.deploy_payload)
