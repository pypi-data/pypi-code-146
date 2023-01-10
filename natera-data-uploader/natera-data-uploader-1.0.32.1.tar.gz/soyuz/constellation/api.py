import json
import logging

import requests

from soyuz.utils import UploaderException


class ConstellationApi(object):
    def __init__(self, token, constellation_url):
        # type: (str, str) -> None

        if not constellation_url:
            raise UploaderException('Constellation API URL was not specified')

        self.__token = token
        self.__url = constellation_url

    def start_upload_job(self, run_folder_name, site_id):
        # type: (str, str) -> str

        logging.info('Creating upload job for {}'.format(run_folder_name))

        try:
            headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.__token)}
            data = json.dumps({'runFolder': run_folder_name, 'siteId': site_id}) if site_id else json.dumps({'runFolder': run_folder_name})

            r = requests.post(url='{}/2.0/jobs/sequencingUpload'.format(self.__url),
                              headers=headers,
                              data=data)

            logging.info('Upload job created: {}'.format(r.text))

            return r.json()['jobId']
        except Exception as e:
            logging.error('Error creating upload job for {} with error: \'{}\''.format(self.__url, e))

    def get_job_status_by_id(self, job_id):
        # type: (str) -> str

        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.__token)}

        return requests.get(
            url='{}/2.0/jobs/sequencingUpload/{}'.format(self.__url, job_id),
            headers=headers).json()['status']
