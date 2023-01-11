import csv
import json
import logging
import os
import shutil
import sys

import yaml

import truera.client.private.metarepo as mr
from truera.client.public.auth_details import AuthDetails
import truera.client.services.artifactrepo_client as ar_cl
from truera.protobuf.aiq.cache_pb2 import \
    ExplanationCacheMetadata as _PBExplanationCacheMetadata
from truera.protobuf.public.aiq import intelligence_service_pb2 as i_s_proto
import truera.protobuf.public.data.data_split_pb2 as d_s_proto
from truera.protobuf.public.metadata_message_types_pb2 import DataProvenance
from truera.protobuf.public.metadata_message_types_pb2 import \
    SplitCreationSource
from truera.rnn.general.model_runner_proxy.general_utils import load_yaml
from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_client import SyncClient
from truera.rnn.general.utils import log
from truera.utils.check_permission_helper import MOCK_REQUEST_CONTEXT
from truera.utils.config_util import get_config_value


def get_parser():
    """Get parser object. These items are specified in the command line"""
    from argparse import ArgumentDefaultsHelpFormatter
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--run_config",
        dest="run_config",
        help="run configuration file",
        metavar="FILE",
        required=True
    )
    parser.add_argument(
        "--repo_config",
        dest="repo_config",
        help="repo configuration file",
        metavar="FILE",
        required=True
    )
    parser.add_argument(
        "--netlens_package_path",
        dest="netlens_package_path",
        help="netlens path",
        default='/home/ubuntu/demo-rnn/lens-api',
        required=False
    )
    return parser


log.configure(logging.INFO)
parser_args = get_parser().parse_args()
args = load_yaml(parser_args.run_config)
sys.path.append(os.path.dirname(parser_args.run_config))
from ingestion_wrappers import DataWrapper
from ingestion_wrappers import ModelWrapper

if (parser_args.netlens_package_path):
    sys.path.insert(0, parser_args.netlens_package_path)
import trulens.nn as netlens

model_locator = Locator.Model(args.project, args.model_name)
model_args = load_yaml(
    os.path.join(os.path.dirname(parser_args.run_config), 'model_config.yaml')
)

from truera.rnn.general.model_runner_proxy.baseline_utils import \
    BaselineConstructor
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    accuracy_filter_func
from truera.rnn.general.model_runner_proxy.mem_utils import save_rnn_model_info
from truera.rnn.general.model_runner_proxy.rnn_attributions import \
    RNNAttribution
from truera.rnn.general.model_runner_proxy.sampling_utils import \
    prepare_datasplit

repo_args = load_yaml(parser_args.repo_config)
sync_client = SyncClient(
    repo_args.sync_client_backend, config_path=parser_args.repo_config
)
log.info(
    'Initialized sync client. \n Backend: {} \n Sync Service: {}'.format(
        sync_client.backend, sync_client.sync_service
    )
)

model_path = sync_client.sync_service.get_cache_path(model_locator)

# CLI will upload the code into a 'code' folder under the model_locator path
model = ModelWrapper.get_model(os.path.join(model_path, 'code'))
from trulens.nn.models import discern_backend

backend = discern_backend(model)
batch_size = 64
log.info('Loaded model.')

log.info("=== Step 1/6: Construct Baseline ===")
baseline_split_locator = Locator.Split(
    args.project, args.data_collection, args.baseline_split
)
baseline_split_path = sync_client.sync_service.get_cache_path(
    baseline_split_locator
)

log.info('Baseline split path: ' + baseline_split_path)

baseline_ds, batch_size, is_unknown_ds_type = prepare_datasplit(
    DataWrapper.get_ds(baseline_split_path),
    backend=backend,
    batch_size=batch_size,
    model=model,
    model_wrapper=ModelWrapper,
    num_take_records=args.n_baseline_records,
    shuffle=args.shuffle_data
)

baseline_constructor = BaselineConstructor(
    baseline_ds, baseline_split_path, model, DataWrapper, ModelWrapper,
    model_args, batch_size
)

batched_baseline = baseline_constructor.construct_avg_baseline()

# Define rnn attributor
rnn_attributor = RNNAttribution()

sample_size = args.n_explain_records
metrics_size = args.n_metrics_records
# increase sample ds if we are using a post model filter because we might have much fewer matches

for split in args.splits:

    log.info("Starting Split: " + split)

    split_locator = Locator.Split(args.project, args.data_collection, split)
    split_path = sync_client.sync_service.get_cache_path(split_locator)

    artifact_split = split
    filter_func = None
    if args.post_model_filter_splits_suffix is not None:
        artifact_split = split + "_" + args.post_model_filter_splits_suffix
        filter_func = accuracy_filter_func(args, ModelWrapper, DataWrapper)

    artifact_locator = Locator.Artifact(
        args.project, args.model_name, args.data_collection, artifact_split
    )
    output_path = sync_client.sync_service.get_cache_path(artifact_locator)
    log.info('Output path:' + output_path)
    os.makedirs(output_path, exist_ok=True)
    feature_names = DataWrapper.get_feature_names(split_path)

    log.info('Adding feature files to artifacts for FE use after sync...')
    with open(
        os.path.join(output_path, 'feature_names.csv'), 'w', newline=''
    ) as feature_file:
        wr = csv.writer(feature_file, quoting=csv.QUOTE_ALL)
        wr.writerow(feature_names)

    with open(
        os.path.join(output_path, 'feature_dict.json'), 'w'
    ) as short_desc_fp:
        json.dump(
            DataWrapper.get_short_feature_descriptions(split_path),
            short_desc_fp
        )
    log.info('Feature name artifacts copied to output path.')

    shutil.copyfile(
        parser_args.run_config, os.path.join(output_path, 'run_config.yaml')
    )
    log.info('Run config copied to output path.')
    metrics_ds, _, _ = prepare_datasplit(
        DataWrapper.get_ds(split_path),
        backend=backend,
        batch_size=batch_size,
        model=model,
        model_wrapper=ModelWrapper,
        shuffle=args.shuffle_data
    )
    split_ds, _, _ = prepare_datasplit(
        DataWrapper.get_ds(split_path),
        backend=backend,
        batch_size=batch_size,
        model=model,
        model_wrapper=ModelWrapper,
        shuffle=args.shuffle_data
    )

    log.info("=== Step 2/6: Save Model Info ===")

    save_rnn_model_info(
        metrics_ds,
        model,
        ModelWrapper,
        DataWrapper,
        metrics_size,
        sample_size,
        output_path,
        model_args,
        backend,
        getattr(args, 'forward_padded', False),
        filter_func=filter_func
    )

    log.info("=== Step 3/6: Input Attributions ===")
    total_records = rnn_attributor.count_records(
        split_ds,
        ModelWrapper,
        model,
        args.n_explain_records,
        backend,
        filter_func=filter_func
    )
    if (is_unknown_ds_type):
        # unknown iterable types may not refresh dataset from the beginning
        split_ds, _, _ = prepare_datasplit(
            DataWrapper.get_ds(split_path),
            backend=backend,
            batch_size=batch_size,
            model=model,
            model_wrapper=ModelWrapper,
            shuffle=args.shuffle_data
        )

    rnn_attributor.calculate_attribution_per_timestep(
        split_ds,
        ModelWrapper,
        model,
        batched_baseline,
        output_path,
        total_records,
        model_args,
        backend,
        filter_func=filter_func,
        input_anchor=model_args.input_anchor,
        output_anchor=model_args.output_anchor
    )

    log.info("=== Step 4/6: Internal Attributions ===")
    if (
        args.n_internal_explain_records is not None and
        args.n_internal_explain_records > 0
    ):
        if (is_unknown_ds_type):
            # unknown iterable types may not refresh dataset from the beginning
            split_ds, _, _ = prepare_datasplit(
                DataWrapper.get_ds(split_path),
                backend=backend,
                batch_size=batch_size,
                model=model,
                model_wrapper=ModelWrapper,
                shuffle=args.shuffle_data
            )
        total_records = rnn_attributor.count_records(
            split_ds,
            ModelWrapper,
            model,
            args.n_internal_explain_records,
            backend,
            filter_func=filter_func
        )

        if (is_unknown_ds_type):
            # unknown iterable types may not refresh dataset from the beginning
            split_ds, _, _ = prepare_datasplit(
                DataWrapper.get_ds(split_path),
                backend=backend,
                batch_size=batch_size,
                model=model,
                model_wrapper=ModelWrapper,
                shuffle=args.shuffle_data
            )

        rnn_attributor.calculate_internal_attribution_per_timestep(
            split_ds,
            ModelWrapper,
            model,
            batch_size,
            output_path,
            total_records,
            model_args,
            backend,
            filter_func=filter_func,
            input_anchor=model_args.input_anchor,
            output_anchor=model_args.output_anchor,
            internal_anchor=model_args.internal_anchor
        )
    else:
        log.info(
            "Skipped, run_config does not contain n_internal_explain_records."
        )

    log.info("=== Step 5/6: Push s3 ===")
    sync_client.sync_service.push(artifact_locator)

    log.info("== Step 6/6: Create artifact metadata for split")

    if repo_args.use_external_services:
        ailens_home_value = os.environ.get('AILENS_HOME', None)
        config_dir = os.path.join(ailens_home_value, "config")
        client_config_file = os.path.join(config_dir, 'clients.yaml')
        with open(client_config_file) as fp:
            clients_config = yaml.safe_load(fp)

        ar_url = get_config_value(clients_config, "artifactrepo", "url")
        auth_details = auth_details = AuthDetails()
        client = ar_cl.ArtifactRepoClient(
            connection_string=ar_url,
            auth_details=auth_details,
            logger=logging.getLogger(__name__),
            use_http=False
        )

        repo_location = client.upload_artifact(
            output_path, args.project, ar_cl.ArtifactType.cache, artifact_split,
            "", []
        ) + "/"

        from uuid import uuid4
        mr_url = get_config_value(clients_config, "metarepo", "url")

        # TODO: Update all endpoints to V2
        mr_client = mr.MetaRepo(mr_url, "v1")

        project_id = mr_client.get_entities(
            request_ctx=MOCK_REQUEST_CONTEXT,
            entity="project",
            params={"name": args.project}
        )[0]["id"]
        model_id = mr_client.get_entities(
            request_ctx=MOCK_REQUEST_CONTEXT,
            entity="model",
            params={
                "project_id": project_id,
                "name": args.model_name
            }
        )[0]["id"]
        data_collection_id = mr_client.get_entities(
            request_ctx=MOCK_REQUEST_CONTEXT,
            entity="dataset",
            params={
                "project_id": project_id,
                "name": args.data_collection
            }
        )[0]["id"]

        split_id = str(uuid4())
        if args.post_model_filter_splits_suffix is not None:
            split_metadata = d_s_proto.DataSplit(
                id=split_id,
                name=artifact_split,
                project_id=project_id,
                dataset_id=data_collection_id,
                split_type="TEST_SPLIT",
                preprocessed_locator=split_path,
                provenance=DataProvenance(
                    split_creation_source=SplitCreationSource.CREATED_FROM_CLI
                )
            ),
            mr.DataSplitDao(mr_client).add_new(
                request_ctx=MOCK_REQUEST_CONTEXT,
                object=split_metadata,
                insert_only=True
            )

        else:
            split_id = mr_client.get_entities(
                request_ctx=MOCK_REQUEST_CONTEXT,
                entity="datasplit",
                params={
                    "project_id": project_id,
                    "name": artifact_split
                }
            )[0]['id']

        explanation_cache_dao = mr.ExplanationCacheMetadataDao(mr_client)
        model_id_proto = i_s_proto.ModelId(
            project_id=project_id, model_id=model_id
        )

        explanation_cache_metadata = _PBExplanationCacheMetadata(
            id=str(uuid4()),
            model_id=model_id_proto,
            intervention_data_split_id=split_id,
            location=repo_location,
            format="freeform",
            generated_by="generate_artifacts"
        )
        explanation_cache_dao.add_new(
            request_ctx=MOCK_REQUEST_CONTEXT,
            object=explanation_cache_metadata,
            insert_only=True
        )

    log.info("=== Complete! ===")
