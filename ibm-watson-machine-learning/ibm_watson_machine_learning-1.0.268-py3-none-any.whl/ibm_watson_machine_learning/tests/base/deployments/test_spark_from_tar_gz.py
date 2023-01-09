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


class TestSparkDeployment(AbstractOnlineDeploymentTest, unittest.TestCase):
    """
    Test case checking the scenario of storing & deploying Spark model
    using object.
    """
    deployment_type = "mllib_3.2"
    software_specification_name = "spark-mllib_3.2"
    model_name = deployment_name = "spark_model_from_object"
    file_name = "drug-selection-model.tgz"
    IS_MODEL = True

    def get_model(self):
        return os.path.join(os.getcwd(), 'base', 'artifacts', 'spark', self.file_name)

    def create_model_props(self):
        return {
            self.wml_client.repository.ModelMetaNames.NAME: self.model_name,
            self.wml_client.repository.ModelMetaNames.TYPE: self.deployment_type,
            self.wml_client.repository.ModelMetaNames.SOFTWARE_SPEC_UID:
                self.wml_client.software_specifications.get_id_by_name(self.software_specification_name),
            self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCES:
                [
                    {
                        'type': 'connection_asset',
                        'connection': {
                            'id': 'not_applicable',
                        },
                        'location': {
                            'bucket': 'not_applicable',
                            'file_name': 'not_applicable'
                        },
                        'schema': {
                            'id': '1',
                            'type': 'struct',
                            'fields': [{
                                'name': 'AGE',
                                'type': 'float',
                                'nullable': True,
                                'metadata': {
                                    'modeling_role': 'target'
                                }
                            }, {
                                'name': 'SEX',
                                'type': 'string',
                                'nullable': True,
                                'metadata': {}
                            }, {
                                'name': 'CHOLESTEROL',
                                'type': 'string',
                                'nullable': True,
                                'metadata': {}
                            }, {
                                'name': 'BP',
                                'type': 'string',
                                'nullable': True,
                                'metadata': {}
                            }, {
                                'name': 'NA',
                                'type': 'float',
                                'nullable': True,
                                'metadata': {}
                            }, {
                                'name': 'K',
                                'type': 'float',
                                'nullable': True,
                                'metadata': {}
                            }]
                        }
                    }
                ]
        }

    def create_scoring_payload(self):
        return {
            self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                "fields": ["AGE", "SEX", "BP", "CHOLESTEROL", "NA", "K"],
                "values": [[20.0, "F", "HIGH", "HIGH", 0.71, 0.07], [55.0, "M", "LOW", "HIGH", 0.71, 0.07]]
            }]
        }



if __name__ == "__main__":
    unittest.main()
