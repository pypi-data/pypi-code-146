# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from testconfig import config
import os
from configparser import ConfigParser


class Properties:

    def __init__(self):

        if 'configs' in config:
            self.user_name = os.environ.get(config['configs']['test_user_name'])
            self.user_password = os.environ.get(config['configs']['test_user_password'])
            self.api_url = os.environ[config['configs']['api_url']]

        else:
            self.config_file_path = 'local.ini'
            self.config = ConfigParser()
            self.config.read(self.config_file_path)
            self.user_name = os.environ.get(self.config.get('configs', 'test_user_name'))
            self.user_password = os.environ.get(self.config.get('configs', 'test_user_password'))
            self.api_url = os.environ.get(self.config.get('configs', 'api_url'))
