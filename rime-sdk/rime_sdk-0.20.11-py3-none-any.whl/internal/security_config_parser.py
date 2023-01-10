"""Parse protos / configs for the RIME file scanning service."""
from rime_sdk.swagger.swagger_client.models import (
    FilescanningHuggingfaceModelInfo,
    FilescanningModelFileInfo,
    FilescanningPytorchModelInfo,
)


def model_info_from_dict(model_info_dict: dict) -> FilescanningModelFileInfo:
    """Convert config to file scan proto."""
    scan_type = model_info_dict.get("scan_type")
    if scan_type is None:
        raise ValueError("The model_file_info must specify a scan type")
    scan_path = model_info_dict.get("scan_path")
    if scan_path is None:
        raise ValueError("The model_file_info must specify a scan path")
    typed_config = FilescanningModelFileInfo()
    if scan_type == "huggingface":
        hf_model_info = FilescanningHuggingfaceModelInfo(scan_path=scan_path)
        typed_config.huggingface_file = hf_model_info
    elif scan_type == "pytorch":
        pytorch_model_info = FilescanningPytorchModelInfo(scan_path=scan_path)
        typed_config.pytorch_file = pytorch_model_info
    else:
        raise ValueError(f"Invalid scan type {scan_type}")
    return typed_config


def convert_model_info_to_dict(model_file_info: FilescanningModelFileInfo) -> dict:
    """Convert file scan proto to config dict."""
    which_file = "pytorch_file" if model_file_info.pytorch_file else "huggingface_file"
    if which_file == "pytorch_file":
        return {
            "scan_type": "pytorch",
            "scan_path": model_file_info.pytorch_file.scan_path,
        }
    elif which_file == "huggingface_file":
        return {
            "scan_type": "huggingface",
            "scan_path": model_file_info.huggingface_file.scan_path,
        }
    else:
        raise ValueError(f"Unknown file info type: {which_file}")
