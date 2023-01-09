#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import unittest


from ibm_watson_machine_learning.tests.base.abstract.abstract_online_deployment_test import AbstractOnlineDeploymentTest


class TestAIFunction(AbstractOnlineDeploymentTest, unittest.TestCase):
    """
    Test case checking the scenario of storing & deploying a Python function
    using compressed file.
    """
    software_specification_name = "runtime-22.2-py3.10"
    model_name = deployment_name = "ai_function_from_gz_test"
    file_name = "ai_function.gz"
    IS_MODEL = False

    def get_model(self):
        return os.path.join(os.getcwd(), 'base', 'artifacts', 'python_function', self.file_name)

    def create_model_props(self):
        return {
            self.wml_client.repository.FunctionMetaNames.NAME: self.model_name,
            self.wml_client.repository.FunctionMetaNames.SOFTWARE_SPEC_UID:
                self.wml_client.software_specifications.get_id_by_name(self.software_specification_name)
        }

    def create_scoring_payload(self):
        return {
            self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                "fields": ["Gender", "Status", "Children", "Age", "Customer_Status"],
                "values": [
                    ["Male", "M", 2, 48, "Inactive"],
                    ["Female", "S", 0, 23, "Inactive"]
                ]
            }]
        }


if __name__ == "__main__":
    unittest.main()
