from cProfile import run
import inspect
import logging
import os
from pathlib import Path
from platform import python_version
import shutil

import cloudpickle
from trulens.nn.models import discern_backend

from truera.client.nn import BaselineType
## TODO: remove pytorch specific
from truera.client.nn.wrappers.torch import Torch
from truera.nlp.general.model_runner_proxy.mem_utils import save_nlp_model_info
from truera.nlp.general.model_runner_proxy.nlp_counterfactuals import \
    calculate_counterfactual
from truera.nlp.general.utils.general_utils import load_module
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    accuracy_filter_func
from truera.rnn.general.model_runner_proxy.general_utils import load_yaml
from truera.rnn.general.model_runner_proxy.sampling_utils import \
    prepare_datasplit
from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_client import SyncClient
from truera.rnn.general.utils import log

log.configure(logging.INFO)


class ArtifactGenerator(object):
    #pylint: disable=E1101
    def __init__(self, parser_args):
        self.parser_args = parser_args

        self.model_args = load_yaml(
            Path(parser_args.run_config).parent / 'model_config.yaml'
        )

        iw_mod = load_module(
            Path(parser_args.run_config).parent, "ingestion_wrappers"
        )

        self.SplitLoadWrapper = iw_mod.CustomNLPSplitLoadWrapper
        self.ModelRunWrapper = iw_mod.CustomNLPModelRunWrapper
        self.ModelLoadWrapper = iw_mod.CustomNLPModelLoadWrapper

        self.repo_args = load_yaml(parser_args.repo_config)
        self.sync_client = SyncClient(
            self.repo_args.sync_client_backend,
            config_path=parser_args.repo_config
        )
        log.info(
            'Initialized sync client. \n Backend: {} \n Sync Service: {}'.
            format(self.sync_client.backend, self.sync_client.sync_service)
        )

        self.run_config = load_yaml(self.parser_args.run_config)
        #pylint: disable=not-callable
        self.model_locator = Locator.Model(
            self.run_config.project, self.run_config.model_name
        )

        self.model_path: Path = Path(
            self.sync_client.sync_service.get_cache_path(self.model_locator)
        )

        # CLI will upload the code into a 'code' folder under the model_locator path
        self.model_code_path = self.model_path / 'code'

    def save_model_to_local(self):
        log.info(
            f'Pickled model using cloudpickle on python {python_version()}. Python versions must match for UI Loading'
        )

        def _save_class_file(path: Path, name: str, class_def):
            path_to_file = path / name

            path_to_file.parent.mkdir(parents=True, exist_ok=True)
            with open(path_to_file, 'wb+') as handle:
                if inspect.isclass(class_def):
                    cloudpickle.dump(class_def, handle)
                else:
                    cloudpickle.dump(class_def.__class__, handle)
            return path_to_file

        _save_class_file(
            self.model_code_path, 'model_run_wrapper.pickle',
            self.ModelRunWrapper
        )
        _save_class_file(
            self.model_code_path, 'model_load_wrapper.pickle',
            self.ModelLoadWrapper
        )

    def generate_artifacts(self):
        run_config = self.run_config

        from truera.nlp.general.model_runner_proxy.nlp_attributions import \
            NLPAttribution

        # Define nlp attributor
        nlp_attributor = NLPAttribution()

        model_run_wrapper = self.ModelRunWrapper()
        # Static methods only but we create instance anyway to simplify typing hints.

        model_load_wrapper = self.ModelLoadWrapper(self.model_code_path)

        model = model_load_wrapper.get_model()
        tokenizer = model_load_wrapper.get_tokenizer(model_run_wrapper.n_tokens)
        vocab_dict = tokenizer.get_vocab()
        #self.save_model_to_local()

        backend = discern_backend(model)
        #pylint: disable=E1101
        batch_size = run_config.batch_size
        log.info('Loaded model and tokenizer.')

        log.info("=== Step 1/4: Construct Baseline ===")
        n_steps = 4
        if self.parser_args.upload:
            n_steps += 2
        log.info(f"=== Step 1/{n_steps}: Construct Baseline ===")
        #pylint: disable=E1101
        baseline_type = BaselineType.from_str(self.model_args.baseline_type)

        if baseline_type != BaselineType.DYNAMIC:
            ###fixed baseline
            batched_baseline = model_run_wrapper.get_baseline(
                model,
                tokenizer,
                n_tokens=model_run_wrapper.n_tokens,
                baseline_type=baseline_type
            )
        else:
            batched_baseline = None  ## to be calculated dynamically for each split
        #pylint: disable=E1101
        for split in run_config.splits:
            log.info("Starting Split: " + split)
            #pylint: disable=E1101
            #pylint: disable=not-callable
            split_locator = Locator.Split(
                run_config.project, run_config.data_collection, split
            )
            split_path_original: Path = Path(
                self.sync_client.sync_service.get_cache_path(split_locator)
            )

            artifact_split = split
            filter_func = None

            if getattr(
                run_config, 'original_post_model_filter_splits_suffix', None
            ) is not None:
                #pylint: disable=E1101
                run_config.post_model_filter_splits_suffix = run_config.original_post_model_filter_splits_suffix
                run_config.post_model_filter_thresh = run_config.original_post_model_filter_thresh
                run_config.post_model_filter_labels = run_config.original_post_model_filter_labels
                artifact_split = split + "_" + run_config.post_model_filter_splits_suffix
                filter_func = accuracy_filter_func(
                    run_config, self.ModelRunWrapper
                )
            #pylint: disable=E1101
            #pylint: disable=not-callable
            artifact_locator = Locator.Artifact(
                run_config.project, run_config.model_name,
                run_config.data_collection, artifact_split
            )

            output_path_original: Path = Path(
                self.sync_client.sync_service.get_cache_path(artifact_locator)
            )
            log.info(f'Output path for original data: {output_path_original}')

            #pylint: disable=E1101
            is_counterfactual_list = [run_config.is_counterfactual]

            ### regenerate original artifacts anyway even if the original artifact folder exists.
            if run_config.is_counterfactual and (
                not output_path_original.exists() or
                run_config.force_regenerate_original_artifacts
            ):
                log.info('Generate the original artifacts first. ')
                is_counterfactual_list = [False, True]

            split_path: Path
            output_path: Path
            process_text: bool
            sample_size: int
            metrics_size: int

            for is_counterfactual in is_counterfactual_list:

                log.info(
                    "===is counterfactual data? {} ===".
                    format(is_counterfactual)
                )
                if is_counterfactual:
                    #pylint: disable=E1101
                    filter_func = None
                    if run_config.counterfactual_post_model_filter_splits_suffix is not None:
                        #pylint: disable=E1101
                        run_config.post_model_filter_splits_suffix = run_config.counterfactual_post_model_filter_splits_suffix
                        run_config.post_model_filter_thresh = run_config.counterfactual_post_model_filter_thresh
                        run_config.post_model_filter_labels = run_config.counterfactual_post_model_filter_labels
                        artifact_split = split + "_" + run_config.post_model_filter_splits_suffix
                        filter_func = accuracy_filter_func(
                            run_config, self.ModelRunWrapper
                        )

                    artifact_split_counterfactual = artifact_split + '_counterfactual'
                    #pylint: disable=E1101
                    #pylint: disable=not-callable
                    artifact_locator = Locator.Artifact(
                        run_config.project, run_config.model_name,
                        run_config.data_collection,
                        artifact_split_counterfactual
                    )
                    output_path: Path = Path(
                        self.sync_client.sync_service.
                        get_cache_path(artifact_locator)
                    )

                    log.info(
                        f'Output path for counterfactual data: {output_path}'
                    )
                    split_path: Path = output_path  ### counterfactual data will be first generated and saved to output_path
                    process_text = False
                    sample_size = run_config.counterfactual_n_explain_records
                    metrics_size = run_config.counterfactual_n_metrics_records

                else:

                    ### parameter settings for do not generate counterfactual artifacts
                    split_path: Path = split_path_original
                    output_path: Path = output_path_original
                    process_text = True
                    sample_size = run_config.n_explain_records
                    metrics_size = run_config.n_metrics_records

                split_load_wrapper = self.SplitLoadWrapper(split_path)

                output_path.mkdir(parents=True, exist_ok=True)

                # This is being copied just to save the run state for debugging purposes.
                shutil.copyfile(
                    self.parser_args.run_config,
                    str(output_path / 'run_config.yaml')
                )
                log.info('Run config copied to output path.')

                if is_counterfactual:
                    ###operations only needed when generating a counterfactual
                    with (output_path /
                          'original_data_path.txt').open('w') as f:
                        f.writelines(
                            f'original_data_artifact_path: {output_path_original}'
                        )  ### saving the path of the original artifact as a meta data
                    ### only generate counterfactual data once after original data artifacts are generated
                    log.info(
                        "=== Generating Counterfactual Data from Original Data ==="
                    )
                    #pylint: disable=no-value-for-parameter
                    calculate_counterfactual(
                        output_path_original,
                        output_path,
                        Torch.get_device()  # TODO tensorflow: pytorch specific?
                    )  # counterfactual requires class qoi influences of the original data.

                log.info("preparing datasplit")
                split_ds, _, _ = prepare_datasplit(
                    split_load_wrapper.get_ds(),
                    backend=backend,
                    batch_size=run_config.batch_size,
                    model=model,
                    model_wrapper=self.ModelRunWrapper,
                    shuffle=run_config.shuffle_data
                )

                log.info(f"=== Step 2/{n_steps}: Save Model Info ===")
                save_nlp_model_info(
                    ds=split_ds,
                    model_run_wrapper=self.ModelRunWrapper,
                    model=model,
                    tokenizer=tokenizer,
                    vocab=vocab_dict,
                    metrics_size=metrics_size,
                    sample_size=sample_size,
                    output_path=output_path,
                    model_config=self.model_args,
                    backend=backend,
                    forward_padded=getattr(run_config, 'forward_padded', False),
                    filter_func=filter_func,
                    split_load_wrapper=self.SplitLoadWrapper,
                )

                # split_ds iterator cannot be iterated twice, so we need to
                # recreate it.
                log.info("preparing datasplit (again)")
                split_ds, _, _ = prepare_datasplit(
                    split_load_wrapper.get_ds(),
                    backend=backend,
                    batch_size=run_config.batch_size,
                    model=model,
                    model_wrapper=self.ModelRunWrapper,
                    shuffle=run_config.shuffle_data
                )

                log.info(f"=== Step 3/{n_steps}: Input Attributions ===")
                total_records = NLPAttribution.count_records(
                    ds=split_ds,
                    model=model,
                    sample_size=sample_size,
                    backend=backend
                )
                gradient_path_records = min(
                    run_config.n_grad_pth_records, total_records
                )

                extra = dict()

                extra['gradient_path_sample_size'] = gradient_path_records
                extra['filter_func'] = filter_func
                #pylint: disable=E1101
                nlp_attributor.calculate_attribution(
                    split_ds=split_ds,  # "ds"
                    batch_size=run_config.batch_size,
                    model=model,
                    tokenizer=tokenizer,
                    model_run_wrapper=self.ModelRunWrapper,
                    baseline_type=baseline_type,
                    baseline=batched_baseline,
                    output_path=output_path,
                    sample_size=total_records,
                    model_args=self.model_args,
                    backend=backend,
                    resolution=self.model_args.resolution,
                    **extra
                )

                nlp_attributor.calculate_attribution_per_original_word(
                    output_path
                )

            log.info(f"=== Step 4/{n_steps}: Push model to backing store ===")
            self.save_model_to_local()
            if self.parser_args.upload:
                log.info(
                    f"=== Step 5/{n_steps}: Push artifacts to backing store ==="
                )
                log.info(f"Backing store is {self.sync_client.backend}")
                self.sync_client.sync_service.push(artifact_locator)

                log.info(
                    f"=== Step 6/{n_steps}: Push model to backing store ==="
                )
                self.sync_client.sync_service.push(self.model_locator)
            else:
                log.info(
                    "Skipping backstore upload, set --upload flag to upload."
                )
