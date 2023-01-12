import os
import logging
import pybpodgui_api
from pybpodgui_api.models.user.user_base import UserBase

from sca.formats import json

logger = logging.getLogger(__name__)


class UserIO(UserBase):

    def __init__(self, _project):
        super(UserIO, self).__init__(_project)

        self.data = None  # DOn't know if we actualy need this

    def save(self):
        if not self.name:
            logger.warning('Skipping user without a name')
            return None
        else:
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            if self.data:
                data = self.data
            else:
                data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a user used on PyBpod GUI.'
                )

            config_path = os.path.join(self.path, self.name + '.json')
            with open(config_path, 'w') as fstream:
                json.dump(data, fstream)

    def toJSON(self):
        data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a user used on PyBpod GUI.'
                )

        return json.dumps(data)

    def load(self, path):
        self.name = os.path.basename(path)

        try:
            with open(os.path.join(self.path, self.name + '.json'), 'r') as stream:
                self.data = data = json.load(stream)
            self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4
        except:
            raise Exception('There was an error loading the configuration file for the subject [{0}]')

    def collect_data(self, data):
        data.update({'name': self.name})
        return data
