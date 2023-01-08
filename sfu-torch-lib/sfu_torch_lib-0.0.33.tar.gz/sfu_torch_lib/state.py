import logging
import os
from typing import Type, Dict, Any, Optional

import mlflow
import torch
from pytorch_lightning import LightningModule

import sfu_torch_lib.io as io


logger = logging.getLogger(__name__)


def get_checkpoint_path(run_id: str, filename: str = 'last') -> Optional[str]:
    run = mlflow.get_run(run_id)

    checkpoint_path = os.path.join(run.info.artifact_uri, f'{filename}.ckpt')

    if not io.exists(checkpoint_path):
        return None

    return checkpoint_path


def get_localized_checkpoint_path(
        run_id: str,
        filename: str = 'last',
        overwrite: bool = True,
        cache: bool = False,
) -> Optional[str]:

    checkpoint_path = get_checkpoint_path(run_id, filename)

    if checkpoint_path is None:
        return None

    basename = f'{run_id}.ckpt'
    checkpoint_path = io.localize_cached(checkpoint_path, basename, overwrite, cache)

    return checkpoint_path


def get_resumable_checkpoint_path(
        run_id: Optional[str],
        restart: bool = False,
        filename: str = 'last',
) -> Optional[str]:

    if restart or not run_id:
        return None

    checkpoint_path = get_localized_checkpoint_path(run_id, filename)

    if not checkpoint_path:
        run = mlflow.get_run(run_id)

        if len(run.data.metrics) > 0:
            logging.warning('Could not find checkpoint. The model will not be initialized.')

    return checkpoint_path


def get_checkpoint(run_id: str, filename: str = 'last') -> Optional[Dict[str, Any]]:
    checkpoint_path = get_checkpoint_path(run_id, filename)

    if checkpoint_path is None:
        return None

    with io.open(checkpoint_path) as checkpoint_file:
        checkpoint = torch.load(checkpoint_file)

    return checkpoint


def load_model(
        run_id: str,
        module_class: Type[LightningModule],
        filename: str = 'last',
        cache: bool = False,
        overwrite: bool = True,
        **kwargs,
) -> LightningModule:

    if cache:
        checkpoint_path = get_localized_checkpoint_path(run_id, filename, overwrite)
    else:
        checkpoint_path = get_checkpoint_path(run_id, filename)

    assert checkpoint_path

    with io.open(checkpoint_path) as checkpoint_file:
        model = module_class.load_from_checkpoint(checkpoint_file, **kwargs)

    assert isinstance(model, LightningModule)

    return model


def load_checkpoint_state(checkpoint_path: str, model: LightningModule, strict: bool = True) -> None:
    device = torch.device('cuda') if torch.cuda.device_count() else torch.device('cpu')

    with io.open(checkpoint_path) as checkpoint_file:
        checkpoint = torch.load(checkpoint_file, device)

    model.load_state_dict(checkpoint['state_dict'], strict)


def load_state(run_id: str, model: LightningModule, filename: str = 'last', strict: bool = True) -> None:
    checkpoint_path = get_localized_checkpoint_path(run_id, filename)

    assert checkpoint_path

    load_checkpoint_state(checkpoint_path, model, strict)
