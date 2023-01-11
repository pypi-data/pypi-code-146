import __main__
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

# from unittest import mock

from cinnaroll_internal import (
    environment_info,
    model,
    post_training_validation,
    pre_training_validation,
    rollout_config,
    utils,
)

from cinnaroll_internal.environment_info import WorkingEnvironment
from cinnaroll_internal.infer_func_deps_finder import output_verification
from cinnaroll_internal.infer_func_deps_finder.deps_finder import build_deps_finder
from cinnaroll_internal.jupyter_notebook import Notebook

from cinnaroll_internal.model_upload import (
    check_size_limits,
    prepare_artifact,
    send_rollout_data,
    upload_artifact,
    notify_server,
)

# from utils import mock_request

CACHE_DIR_NAME = ".cinnaroll_cache"
# for tf/keras it's a dir, otherwise file
MODEL_SAVE_FILE_OR_DIR_NAME = "saved_model"
ARTIFACT_FILE_NAME = "artifact.tar.gz"
TRAIN_EVAL_CODE_FILE_NAME = "train_eval_code.py"


class RolloutConfigurationError(Exception):
    ...


# todo: if dict config is chosen, refactor this to return RolloutConfig and errors
# get stuff, don't transform data but return errors if something besides metrics is missing (key errors and None values)
# try to create RolloutConfig out of what's in dict
# catch type errors and reformat them to make them easier to understand
# return RolloutConfig and errors
def get_config_from_dict(
    config: Dict[str, Any]
) -> Tuple[rollout_config.RolloutConfig, List[Exception]]:
    pass


# todo: e2es on real filesystem to check multiplatform compatibility
def get_cache_dir_path(working_environment: WorkingEnvironment, current_notebook: Optional[Notebook]) -> Path:
    if working_environment is WorkingEnvironment.SCRIPT:
        return Path(__main__.__file__).parent / CACHE_DIR_NAME
    if working_environment is working_environment.NOTEBOOK:
        if not current_notebook:
            raise RuntimeError
        return Path(current_notebook.path).parent / CACHE_DIR_NAME
    if working_environment is working_environment.GOOGLE_COLAB:
        return Path(CACHE_DIR_NAME)
    raise environment_info.UnknownEnvironmentError


def create_cache_dir_if_not_exists(cache_dir_path: Path) -> None:
    if not cache_dir_path.exists():
        cache_dir_path.mkdir()


def cut_dataset_from_metrics(config: rollout_config.RolloutConfig) -> Optional[str]:
    if config.metrics:
        if "dataset" in config.metrics:
            dataset_tag = str(config.metrics["dataset"])
            del config.metrics["dataset"]
            return dataset_tag
    return None


# @mock.patch("requests.get", utils.mock_request)
# @mock.patch("requests.post", utils.mock_request)
# @mock.patch("requests.put", utils.mock_request)
def rollout(config: rollout_config.RolloutConfig) -> None:
    print("Validating config pre-training...")
    pre_training_errors = pre_training_validation.find_config_pre_training_errors(
        config
    )

    if len(pre_training_errors):
        for e in pre_training_errors:
            print(repr(e))
        raise RolloutConfigurationError
    print("Pre-training validation OK! Great!")

    working_environment, current_notebook = environment_info.get_working_environment_and_notebook_if_appropriate()
    cache_dir_path = get_cache_dir_path(working_environment, current_notebook)
    create_cache_dir_if_not_exists(cache_dir_path)

    model_save_path = cache_dir_path / MODEL_SAVE_FILE_OR_DIR_NAME
    artifact_path = cache_dir_path / ARTIFACT_FILE_NAME
    train_eval_code_path = cache_dir_path / TRAIN_EVAL_CODE_FILE_NAME

    print("Inferring framework...")
    framework = model.infer_framework(config.model_object)
    cinnaroll_model = model.create_model(config.model_object, framework, model_save_path)

    trained_in_script = model.is_trained_in_script(config.train_eval)

    # if train_eval it not empty by default we want to train model
    train_model = trained_in_script
    try:
        with open(train_eval_code_path, "r") as train_eval_code_file:
            cached_train_eval_code = train_eval_code_file.read()
    except OSError:
        cached_train_eval_code = ""

    current_train_eval_code = utils.get_function_code_without_comments(config.train_eval)

    if trained_in_script:
        if cached_train_eval_code == current_train_eval_code:
            if cinnaroll_model.is_equal_to_cached():
                train_model = False

                print("Loading saved model...")
                try:
                    # if model exists and can be loaded we do not want to train it
                    cinnaroll_model.load()
                except model.ModelLoadingError as e:
                    # if model exists but loading fails and train_val is not empty, we ask the user to decide
                    if trained_in_script:
                        user_input = ""

                        while user_input not in ("y", "yes", "n", "no"):
                            user_input = input(
                                f"Loading the model failed with the following error: {repr(e)} Train? y/n "
                            )
                            if user_input in ("y", "yes"):
                                train_model = True
                else:
                    print("Loaded successfully!")

    if train_model:
        with open(train_eval_code_path, "w") as train_eval_code_file:
            train_eval_code_file.write(current_train_eval_code)

        print("Training model...")
        config.metrics = config.train_eval(config.model_object)
        print("Model trained!")

    print("Saving model...")
    try:
        cinnaroll_model.save()
    except model.ModelSavingError as e:
        print(f"Saving the model failed with the following error: {repr(e)}")
    else:
        print("Model saved!")

    print("Validating config post-training...")

    post_training_errors = post_training_validation.find_config_post_training_errors(
        cinnaroll_model=cinnaroll_model,
        config=config,
    )

    if len(post_training_errors):
        for err in post_training_errors:
            print(repr(err))
        raise RolloutConfigurationError
    print("Post-training validation OK! Great!")

    # print("Fetching model metadata...")

    # model_metadata = cinnaroll_model.get_metadata()
    print("Fetching environment info...")
    user_environment_info = environment_info.EnvironmentInfo(framework)

    print("Creating model artifact...")
    print("  * Fetching infer function code and dependencies...")
    deps_finder = build_deps_finder(current_notebook, config)
    infer = deps_finder.get_infer_with_used_global_variables()
    print("  * Verifying generated code works correctly...")
    output_verification.verify_infer_works_for_sample_input(
        infer.test_file_content, infer.global_variables, config, cache_dir_path
    )
    print("  * Generated code looks good!")

    size_limit_errors = check_size_limits(
        infer.output_file_content,
        config.model_input_sample,
        config.infer_func_input_sample,
        config.infer_func_input_format,
    )

    if len(size_limit_errors) > 0:
        for err in size_limit_errors:
            print(repr(err))
        raise RolloutConfigurationError
    print("Size limit checks of individual components passed.")

    artifact_preparation_errors = prepare_artifact(
        artifact_path,
        model_save_path,
        infer.output_file_content,
        infer.global_variables,
        user_environment_info.requirements,
        config.model_input_sample,
        config.infer_func_input_sample,
        config.infer_func_input_format,
    )

    if len(artifact_preparation_errors) > 0:
        for err in artifact_preparation_errors:
            print(repr(err))
        raise RolloutConfigurationError
    print("Artifact prepared correctly.")

    if 'CINNAROLL_SKIP_MODEL_UPLOAD' in os.environ:
        utils.clean_path(cache_dir_path)
        return

    print("Sending rollout data to cinnaroll backend...")

    model_metadata: Dict[str, str] = {}
    dataset_name = cut_dataset_from_metrics(config)
    if dataset_name:
        model_metadata['dataset'] = dataset_name

    res = send_rollout_data(
        config=config,
        framework=framework,
        user_environment_info=user_environment_info,
        model_metadata=model_metadata,
    )

    if res.status_code != 200:
        raise RolloutConfigurationError(f"Sending rollout data failed with "
                                        f"error code {res.status_code} and reason: {res.reason}")

    res_json = res.json()
    upload_id = res_json["id"]
    upload_url = res_json["uploadUrl"]

    print("Uploading model and input samples...")
    res_upload_artifact = upload_artifact(artifact_path, upload_url)

    if res_upload_artifact.status_code == 200:
        status = "UPLOAD_SUCCESSFUL"
    else:
        status = "UPLOAD_FAILED"

    res_notify_server = notify_server(upload_id, status)

    if res_upload_artifact.status_code != 200:
        raise RolloutConfigurationError("Artifact upload failed with "
                                        f"error code {res_upload_artifact.status_code} "
                                        f"and reason: {res_upload_artifact.reason}")

    if res_notify_server.status_code != 200:
        raise RolloutConfigurationError("Post-upload server notification failed with "
                                        f"error code {res_notify_server.status_code} "
                                        f"and reason: {res_notify_server.reason}")

    print("Success!")
    print("Congratulations! You've configured cinnaroll rollout successfully!")

    utils.clean_path(cache_dir_path)
