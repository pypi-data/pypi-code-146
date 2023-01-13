import json
import logging
import tarfile
import tempfile
from typing import Any, Callable, Optional, Tuple

from colorama import Fore, Style
from truss.build import create
from truss.local.local_config_handler import \
    LocalConfigHandler as TrussLocalConfigHandler
from truss.truss_handle import TrussHandle

import baseten
from baseten.baseten_deployed_model import BasetenDeployedModel
from baseten.common import api, settings
from baseten.common.core import MODEL_FILENAME, Semver, raises_api_error
from baseten.common.util import base64_encoded_json_str

logger = logging.getLogger(__name__)


def _exists_model(
    model_name: Optional[str],
    model_id: Optional[str],
    models_provider: Callable
) -> Optional[Tuple[str, str]]:
    """Checks if an effective model exists for the purpose of deploy or one needs to be created.

    If model name is supplied and a model with that name exists then it's picked up. Otherwise
    working model id in the session is tried.

    Returns id of model if model exists, or None
    """
    models = models_provider()["models"]
    model_id_by_name = {model["name"]: model["id"] for model in models}
    model_name_by_id = {model["id"]: model["name"] for model in models}

    if model_name is not None:
        if model_name in model_id_by_name:
            return model_id_by_name[model_name], model_name
        else:
            logger.warning("Model name not found in deployed models")
            return None

    # No model_name supplied, try to work with working model id
    if model_id is not None:
        if model_id in model_name_by_id:
            return model_id, model_name_by_id[model_id]
        else:
            logger.warning("Working model id not found in deployed models")
            return None

    # No model name or working model
    return None


def build_truss(
    model: Any,
    target_directory: Optional[str] = None,
) -> TrussHandle:
    """
    Builds truss into target directory from in-memory model
    Args:
        model (an in-memory model object): A model object to be deployed (e.g. a keras,
            sklearn, or pytorch model object)
        target_directory (str, optional): The local directory target for the truss.
            Otherwise a temporary directory will be generated
    Returns:
        TrussHandle
    """
    truss = create(model=model, target_directory=target_directory)

    truss_help_messages = f"""
    --------------------------------------------------------------------------------------------
    | {Fore.BLUE} Autogenerating Truss for your model, find more about Truss at https://truss.baseten.co/ |
    --------------------------------------------------------------------------------------------
    You can find your auto generated Truss at {Fore.BLUE} {str(truss.spec.truss_dir.resolve())}
    ---------------------------------------------------------------
    | {Fore.BLUE} Some useful commands to work with your Truss... |
    ---------------------------------------------------------------
    To load your Truss, you can either
    1. Access the Truss handle via the object returned by this function via {Fore.MAGENTA} deployed_model.truss
    2. Load the Truss handle via {Fore.MAGENTA} handle = truss.load('{str(truss.spec.truss_dir.resolve())}')
    To locally run your Truss before deploying, run {Fore.MAGENTA} handle.predict(test_input)
    To add a requirement to your Truss, run {Fore.MAGENTA} handle.add_python_requirement('numpy')
    Visit the docs to learn more about Truss!
    """
    for msg in truss_help_messages.splitlines():
        logger.info(msg.strip())
    return truss


@raises_api_error
def deploy_truss(
    b10_truss: TrussHandle,
    model_name: Optional[str] = None,
    semver_bump: str = Semver.MINOR.value,
    is_trusted=False,
    is_draft=False,
    external_model_version_id=None,
) -> BasetenDeployedModel:
    """
    Given an existing baseten truss object, deploy it onto the baseten infastructure.

    Args:
        b10_truss: A truss object representing a local baseten_truss directory
        model_name (str, optional): The name of the model to be created, if necessary.
        semver_bump (str, optional): The version bump for this deployment, one of 'MAJOR', 'MINOR', 'PATCH'.
        is_trusted (bool, optional): Whether or not to mark a truss as `trusted` on Baseten.

    Returns:
        BasetenDeployedModel
    """
    if model_name is None:
        import coolname
        model_name = coolname.generate_slug(2)

    elif not model_name or model_name.isspace():
        raise ValueError("Model Names cannot be empty or spaces")

    # TODO(pankaj) The exists check after generating random name is incorrect.
    # If we happen to generate a random name that's already taken then we will
    # have unexpected behavior.
    model_info = _exists_model(model_name, baseten.working_model_id, api.models)

    if model_info is not None and is_draft:
        version_info = try_patch_draft_truss(model_name, b10_truss)
        if version_info is not None:
            model_id, model_name = model_info
            model_version_id = version_info["id"]
            return BasetenDeployedModel(
                model_version_id=model_version_id, model_name=model_name, truss_handle=b10_truss
            )

    logger.info(f"Serializing {Fore.BLUE}{model_name}{Style.RESET_ALL} truss.")
    temp_file = _compress_truss(b10_truss=b10_truss)
    logger.info("Making contact with BaseTen 👋 👽")
    s3_key = api.upload_model(temp_file, "tgz", MODEL_FILENAME)
    # String that can be passed through graphql api
    config = base64_encoded_json_str(b10_truss._spec._config.to_dict())
    if is_draft:
        model_id, model_version_id = deploy_draft_truss(
            model_name=model_name,
            s3_key=s3_key,
            config=config,
            is_trusted=is_trusted,
        )
    else:
        if not model_info:
            model_id, model_version_id = create_model_from_s3(
                model_name, s3_key, config, semver_bump, is_trusted, external_model_version_id
            )
            logger.info(
                f"Successfully registered model {Fore.BLUE}{model_name}{Style.RESET_ALL}."
            )
        else:
            model_id, model_name = model_info
            model_version_id = create_model_version_from_s3(
                model_id, s3_key, config, semver_bump, is_trusted, external_model_version_id)
            logger.info(
                f"Successfully created version {Fore.BLUE}{model_version_id}{Style.RESET_ALL} for {model_name}."
            )

    _generate_model_deploy_logs(model_id)
    return BasetenDeployedModel(
        model_version_id=model_version_id, model_name=model_name, truss_handle=b10_truss
    )


def deploy_draft_truss(
        model_name,
        s3_key,
        config,
        is_trusted=False,
):
    model_version_json = api.deploy_draft_truss(
        model_name=model_name,
        s3_key=s3_key,
        config=config,
        client_version=baseten.__version__,
        is_trusted=is_trusted,
    )

    logger.info(
        f"Created model:\n{json.dumps(model_version_json, indent=4)}"
    )
    model_id = model_version_json["id"]
    model_version_id = model_version_json["version_id"]
    # Set the newly created model model_version_json
    # be the working model for future commands
    baseten.working_model_id = model_id

    return model_id, model_version_id


def try_patch_draft_truss(
    model_name: str,
    truss_handle: TrussHandle,
) -> Optional[dict]:
    dev_model_version_info = _get_draft_model_version_info(model_name)
    if dev_model_version_info is None:
        logger.info(f"Giving up on patching: no draft model found for model {model_name}.")
        return None

    truss_hash = dev_model_version_info["truss_hash"]
    if truss_hash is None:
        logger.info(f"Giving up on patching: no truss_hash found for model {model_name}.")
        return None

    truss_signature = dev_model_version_info["truss_signature"]
    if truss_signature is None:
        logger.info(f"Giving up on patching: no truss_signature found for model {model_name}.")
        return None

    TrussLocalConfigHandler.add_signature(truss_hash, truss_signature)

    patch_request = truss_handle.calc_patch(truss_hash)
    if patch_request is None:
        logger.info("Giving up on patching: unable to calculate patch.")
        return None

    if patch_request.prev_hash == patch_request.next_hash:
        logger.info("No changes observed skipping deploy")
        return dev_model_version_info

    if len(patch_request.patch_ops) == 0:
        # This shouldn't normally happen, hash check should catch this.
        # Fallback to full deploy.
        logger.info("Giving up on patching: no patchable changes found.")
        return None

    resp = api.patch_draft_truss(
        model_name=model_name,
        client_version=baseten.__version__,
        patch=patch_request,
    )
    if resp['succeeded'] is False:
        logger.info("Giving up on patching: Backend unable to patch.")
        return None

    logger.info(f"Successfully patched draft version of model `{model_name}`.")
    return dev_model_version_info


def _get_draft_model_version_info(model_name) -> Optional[dict]:
    model = api.get_model(model_name)
    versions = model["model_version"]["oracle"]["versions"]
    for version in versions:
        if version["is_draft"] is True:
            return version
    return None


def create_model_from_s3(
        model_name,
        s3_key,
        config,
        semver_bump,
        is_trusted=False,
        external_model_version_id=None,
):
    model_version_json = api.create_model_from_truss(
        model_name=model_name,
        s3_key=s3_key,
        config=config,
        semver_bump=semver_bump,
        client_version=baseten.__version__,
        is_trusted=is_trusted,
        external_model_version_id=external_model_version_id,
    )

    logger.info(
        f"Created model:\n{json.dumps(model_version_json, indent=4)}"
    )
    model_id = model_version_json["id"]
    model_version_id = model_version_json["version_id"]
    # Set the newly created model model_version_json
    # be the working model for future commands
    baseten.working_model_id = model_id

    return model_id, model_version_id


def create_model_version_from_s3(
        model_id,
        s3_key,
        config,
        semver_bump,
        is_trusted=False,
        external_model_version_id=None,
):
    model_version_json = api.create_model_version_from_truss(
        model_id=model_id,
        s3_key=s3_key,
        config=config,
        semver_bump=semver_bump,
        client_version=baseten.__version__,
        is_trusted=is_trusted,
        external_model_version_id=external_model_version_id,
    )
    model_version_id = model_version_json["id"]
    return model_version_id


def _generate_model_deploy_logs(model_id):
    logger.info(f"{Fore.BLUE} Deploying model version.")
    model_version_web_url = f"{settings.get_server_url()}/models/{model_id}"
    logger.info("🏁 The model is being built and deployed right now 🏁")
    visit_message = f"|  Visit {Fore.BLUE}{model_version_web_url}{Style.RESET_ALL} for deployment status  |"
    visit_message_len = len(visit_message) - len(Fore.BLUE) - len(Style.RESET_ALL)
    logger.info("".join(["-" for _ in range(visit_message_len)]))
    logger.info(visit_message)
    logger.info("".join(["-" for _ in range(visit_message_len)]))


def _create_temporary_file(b10_truss, delete=True):
    temp_file = tempfile.NamedTemporaryFile(suffix=".tgz", delete=delete)
    with tarfile.open(temp_file.name, "w:gz") as tar:
        tar.add(b10_truss._spec.truss_dir, arcname=".")
    return temp_file


def _compress_truss(b10_truss):
    try:
        temp_file = _create_temporary_file(b10_truss)
    except PermissionError:
        # Windows bug with Tempfile causes PermissionErrors
        temp_file = _create_temporary_file(b10_truss, delete=False)
    temp_file.file.seek(0)
    return temp_file


def build_and_deploy_truss(
    model: Any,
    model_name: Optional[str] = None,
    version_bump=Semver.MINOR.value,
    is_trusted=False,
    is_draft=False,
    external_model_version_id=None,
) -> BasetenDeployedModel:
    if isinstance(model, TrussHandle):
        return deploy_truss(model, model_name, version_bump, is_trusted, is_draft, external_model_version_id)
    truss = build_truss(model)
    return deploy_truss(truss, model_name, version_bump, is_trusted, is_draft, external_model_version_id)


def pull_model(model_version_id: str, directory: str = "."):
    deployed_model = BasetenDeployedModel(model_version_id=model_version_id)
    return deployed_model.pull(directory)
