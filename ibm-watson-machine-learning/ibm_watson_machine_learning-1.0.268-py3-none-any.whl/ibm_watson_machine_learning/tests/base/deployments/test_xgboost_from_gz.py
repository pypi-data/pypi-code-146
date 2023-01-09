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

import scipy

from ibm_watson_machine_learning.tests.base.abstract.abstract_online_deployment_test import AbstractOnlineDeploymentTest


class TestXGBoostDeployment(AbstractOnlineDeploymentTest, unittest.TestCase):
    """
    Test case checking the scenario of storing & deploying xgboost
    using compressed_file.
    """
    deployment_type = "xgboost_1.6"
    software_specification_name = "runtime-22.2-py3.10"
    model_name = deployment_name = "xgboost_model_from_gz"
    file_name = 'xgboost_model.tar.gz'
    IS_MODEL = True

    def get_model(self):
        return os.path.join(os.getcwd(), 'base', 'artifacts', 'xgboost', self.file_name)

    def create_model_props(self):
        return {
            self.wml_client.repository.ModelMetaNames.NAME: self.model_name,
            self.wml_client.repository.ModelMetaNames.TYPE: self.deployment_type,
            self.wml_client.repository.ModelMetaNames.SOFTWARE_SPEC_UID:
                self.wml_client.software_specifications.get_id_by_name(self.software_specification_name)
        }

    def create_scoring_payload(self):
        data_path = os.path.join(os.getcwd(), 'base', 'datasets', 'xgboost', 'agaricus.txt.test')

        labels = []
        row = []
        col = []
        dat = []
        with open(data_path) as f:
            for i, l in enumerate(f):
                arr = l.split()
                labels.append(int(arr[0]))
                for it in arr[1:]:
                    k, v = it.split(':')
                    row.append(i)
                    col.append(int(k))
                    dat.append(float(v))
        csr = scipy.sparse.csr_matrix((dat, (row, col)))
        return {
            self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                'values': csr.getrow(0).toarray().tolist()
            }]
        }


if __name__ == "__main__":
    unittest.main()
