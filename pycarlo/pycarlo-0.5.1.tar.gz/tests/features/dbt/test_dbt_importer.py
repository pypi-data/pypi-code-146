import json
import os
import pathlib
from typing import Dict
from unittest import TestCase
from unittest.mock import Mock, patch, call
from uuid import uuid4

import requests
from box import Box
from requests import HTTPError, Response

from pycarlo.common.files import BytesFileReader, JsonFileReader
from pycarlo.features.dbt import DbtImporter
from pycarlo.features.dbt.queries import (
    GET_DBT_UPLOAD_URL,
    IMPORT_DBT_MANIFEST,
    IMPORT_DBT_RUN_RESULTS,
    SEND_DBT_ARTIFACTS_EVENT,
    UPLOAD_DBT_MANIFEST,
    UPLOAD_DBT_RUN_RESULTS,
)
from pycarlo.features.pii import PiiFilterer
from pycarlo.features.user import Resource


class DbtImportServiceTest(TestCase):

    manifest_path = f'{pathlib.Path(__file__).parent}/sample_manifest.json'
    run_results_path = f'{pathlib.Path(__file__).parent}/sample_run_results.json'
    logs_path =f'{pathlib.Path(__file__).parent}/sample_logs.txt'

    def setUp(self) -> None:
        self._mock_pii_service = Mock()
        self._mock_pii_service.get_pii_filters_config.return_value = None

    @patch('pycarlo.features.dbt.dbt_importer.http')
    def test_import_run(self, mock_http: Mock):
        # given
        resource = Resource(id=uuid4(), name='Snowflake', type='snowflake')
        mock_user_service = Mock()
        mock_user_service.get_resource.return_value = resource

        def mock_client_responses(**kwargs):
            query = kwargs['query']
            if query == GET_DBT_UPLOAD_URL:
                return Box({
                    'get_dbt_upload_url': f"https://{kwargs['variables']['fileName']}"
                })

        mock_client = Mock(side_effect=mock_client_responses)

        importer = DbtImporter(
            mc_client=mock_client,
            user_service=mock_user_service,
            pii_service=self._mock_pii_service,
        )

        # when
        importer.import_run(
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=resource.id
        )

        # verify expected call to user service
        mock_user_service.get_resource.assert_called_once_with(resource.id)

        # verify expected calls to upload artifacts to S3
        self.assertEqual(3, mock_http.upload.call_count)
        mock_http.upload.assert_has_calls([
            call(
                method='put',
                url='https://sample_manifest.json',
                content=JsonFileReader(self.manifest_path).read()
            ),
            call(
                method='put',
                url='https://sample_run_results.json',
                content=JsonFileReader(self.run_results_path).read()
            ),
            call(
                method='put',
                url='https://sample_logs.txt',
                content=BytesFileReader(self.logs_path).read()
            )
        ])

        # verify expected MC client calls
        self.assertEqual(4, mock_client.call_count)
        mock_client.assert_has_calls([
            call(
                query=GET_DBT_UPLOAD_URL,
                variables=dict(
                    projectName='default-project',
                    invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                    fileName='sample_manifest.json'
                )
            ),
            call(
                query=GET_DBT_UPLOAD_URL,
                variables=dict(
                    projectName='default-project',
                    invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                    fileName='sample_run_results.json'
                )
            ),
            call(
                query=GET_DBT_UPLOAD_URL,
                variables=dict(
                    projectName='default-project',
                    invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                    fileName='sample_logs.txt'
                )
            ),
            call(
                query=SEND_DBT_ARTIFACTS_EVENT,
                variables=dict(
                    projectName='default-project',
                    jobName='default-job',
                    invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                    artifacts=dict(
                        manifest='sample_manifest.json',
                        runResults='sample_run_results.json',
                        logs='sample_logs.txt'
                    ),
                    resourceId=str(resource.id)
                )
            )
        ])

    def test_import_dbt_manifest(self):
        self._client_mock = Mock(return_value=Box({
            'import_dbt_manifest': {
                'response': {
                    'node_ids_imported': [
                        "model.analytics.metric_types",
                        "model.analytics.recent_metrics",
                        "model.analytics.lineage_nodes"
                    ]
                }
            }
        }))

        service = DbtImporter(
            mc_client=self._client_mock,
            pii_service=self._mock_pii_service,
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')
        node_ids_imported = service.import_dbt_manifest(manifest_file, default_resource='snowflake')

        with open(manifest_file, 'r') as f:
            dbt_manifest = Box(json.load(f))

        self._client_mock.assert_called_once_with(
            query=IMPORT_DBT_MANIFEST,
            variables=dict(
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/manifest/v2.json',
                manifestNodesJson=json.dumps(dbt_manifest.nodes.to_dict()),
                projectName=None,
                defaultResource='snowflake'
            )
        )

        self.assertEqual(
            node_ids_imported,
            ['model.analytics.metric_types', 'model.analytics.recent_metrics', 'model.analytics.lineage_nodes']
        )

    def test_import_dbt_manifest_retry(self):
        def create_responses(*args, **kwargs):
            nodes = json.loads(kwargs['variables']['manifestNodesJson'])

            if len(list(nodes.items())) == 1:
                return Box({
                    'import_dbt_manifest': {
                        'response': {
                            'node_ids_imported': [list(nodes.keys())[0]]
                        }
                    }
                })

            response = Response()
            response.status_code = requests.codes.gateway_timeout

            raise HTTPError(response=response)

        self._client_mock = Mock(side_effect=create_responses)

        importer = DbtImporter(
            mc_client=self._client_mock,
            pii_service=self._mock_pii_service,
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')
        node_ids_imported = importer.import_dbt_manifest(manifest_file)

        # client call will timeout, then will send each one-by-one
        # client will be called a total of 4 times
        self.assertEqual(4, self._client_mock.call_count)

        self.assertEqual(
            node_ids_imported,
            ['model.analytics.metric_types', 'model.analytics.recent_metrics', 'model.analytics.lineage_nodes']
        )

    def test_import_dbt_manifest_retry_bail_out(self):
        def create_responses(*args, **kwargs):
            response = Response()
            response.status_code = requests.codes.gateway_timeout

            raise HTTPError(response=response)

        self._client_mock = Mock(side_effect=create_responses)

        importer = DbtImporter(
            mc_client=self._client_mock,
            pii_service=self._mock_pii_service,
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')

        with self.assertRaises(RuntimeError):
            node_ids_imported = importer.import_dbt_manifest(manifest_file)

        # make_request_v2() will always timeout
        # First request will time out
        # Then the next will time out, which has a batch size of 1, at which point it bails out
        self.assertEqual(2, self._client_mock.call_count)

    def test_import_dbt_run_results(self):
        self._client_mock = Mock(return_value=Box({
            'import_dbt_run_results': {
                'response': {
                    'num_results_imported': 4
                }
            }
        }))

        service = DbtImporter(
            mc_client=self._client_mock,
            pii_service=self._mock_pii_service,
        )

        run_results_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_run_results.json')
        with open(run_results_file, 'r') as f:
            run_results = Box(json.load(f))

        node_ids_imported = service.import_run_results(run_results_file)

        self._client_mock.assert_called_once_with(
            query=IMPORT_DBT_RUN_RESULTS,
            variables=dict(
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/run-results/v2.json',
                runResultsJson=json.dumps(run_results),
                projectName=None,
                runId=None,
                runLogs=None
            )
        )

        self.assertEqual(node_ids_imported, 4)

    def test_upload_dbt_manifest(self):
        # given
        project_name = 'mydb'
        resource_name = 'mywarehouse'
        batch_size = 2

        logs = []

        self._client_mock = Mock()
        service = DbtImporter(
            mc_client=self._client_mock,
            print_func=lambda m: logs.append(m),
            pii_service=self._mock_pii_service,
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')
        with open(manifest_file, 'r') as f:
            dbt_manifest = Box(json.load(f))

        all_nodes = dbt_manifest.nodes.to_dict()
        batch_1_nodes = dict(list(all_nodes.items())[:batch_size])
        batch_2_nodes = dict(list(all_nodes.items())[batch_size:])

        # when
        service.upload_dbt_manifest(
            dbt_manifest=manifest_file,
            project_name=project_name,
            default_resource=resource_name,
            batch_size=batch_size)

        # verify expected calls to MC client
        calls = self._client_mock.call_args_list
        self.assertEqual(2, len(calls))

        self.assertDictEqual(dict(
            query=UPLOAD_DBT_MANIFEST,
            variables=dict(
                invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                batch=1,
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/manifest/v2.json',
                manifestNodesJson=json.dumps(batch_1_nodes),
                projectName='mydb',
                defaultResource='mywarehouse'
            )
        ), calls[0][1])

        self.assertDictEqual(dict(
            query=UPLOAD_DBT_MANIFEST,
            variables=dict(
                invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                batch=2,
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/manifest/v2.json',
                manifestNodesJson=json.dumps(batch_2_nodes),
                projectName='mydb',
                defaultResource='mywarehouse'
            )
        ), calls[1][1])

        # verify expected logging
        self.assertEqual(3, len(logs))
        self.assertListEqual([
            'Uploading 3 DBT objects to Monte Carlo for processing. Please wait...',
            'Uploaded 2 objects',
            'Uploaded 3 objects'
        ], logs)

    def test_upload_dbt_run_results(self):
        expected_run_results = JsonFileReader(self.run_results_path).read()
        self.perform_test_upload_run_results(expected_run_results=expected_run_results)

    @patch("pycarlo.features.dbt.DbtImporter._init_pii_filterer")
    def test_upload_dbt_run_results_filtered(self, mock_init_filterer: Mock):
        mock_init_filterer.return_value = PiiFilterer(filters_config={
            'active': [
                {
                    'name': 'thread-id',
                    'pattern': r'Thread-\d{2}'
                }
            ]
        }, include_metrics=False)

        expected_run_results = JsonFileReader(self.run_results_path).read()
        for r in expected_run_results['results']:
            r['thread_id'] = '<filtered:thread-id>'

        self.perform_test_upload_run_results(expected_run_results=expected_run_results)

    def perform_test_upload_run_results(self, expected_run_results: Dict):
        self._client_mock = Mock()
        service = DbtImporter(mc_client=self._client_mock, pii_service=self._mock_pii_service)

        run_results = JsonFileReader(self.run_results_path).read()
        service.upload_run_results(run_results)

        self._client_mock.assert_called_once_with(
            query=UPLOAD_DBT_RUN_RESULTS,
            variables=dict(
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/run-results/v2.json',
                runResultsJson=json.dumps(expected_run_results),
                invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                projectName=None,
                runId=None,
                runLogs=None
            )
        )


    @patch('pycarlo.features.dbt.dbt_importer.http')
    @patch("pycarlo.features.dbt.DbtImporter._init_pii_filterer")
    def test_import_run_filtered(self, mock_init_filterer: Mock, mock_http: Mock):
        resource = Resource(id=uuid4(), name='Snowflake', type='snowflake')
        mock_user_service = Mock()
        mock_user_service.get_resource.return_value = resource

        mock_init_filterer.return_value = PiiFilterer(filters_config={
            'active': [
                {
                    'name': 'thread-id',
                    'pattern': r'Thread-\d{2}'
                }
            ]
        }, include_metrics=False)

        def mock_client_responses(**kwargs):
            query = kwargs['query']
            if query == GET_DBT_UPLOAD_URL:
                return Box({
                    'get_dbt_upload_url': f"https://{kwargs['variables']['fileName']}"
                })

        mock_client = Mock(side_effect=mock_client_responses)

        importer = DbtImporter(
            mc_client=mock_client,
            user_service=mock_user_service,
            pii_service=self._mock_pii_service,
        )

        # when
        importer.import_run(
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=resource.id
        )

        expected_run_results = JsonFileReader(self.run_results_path).read()
        for r in expected_run_results['results']:
            r['thread_id'] = '<filtered:thread-id>'

        # verify call was properly filtered, we know there are thread ids in sample run results
        mock_http.upload.assert_has_calls([
            call(
                method='put',
                url='https://sample_run_results.json',
                content=expected_run_results
            ),
        ])
