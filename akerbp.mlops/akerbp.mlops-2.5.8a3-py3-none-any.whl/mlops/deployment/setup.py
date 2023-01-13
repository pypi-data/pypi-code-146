# setup.py
from pathlib import Path
import logging
from logging import config as logging_config
from akerbp.mlops.core.logger_config import LOGGING_CONFIG
from akerbp.mlops import __version__ as version
from akerbp.mlops.core.config import (
    generate_default_project_settings,
    validate_user_settings,
)
from akerbp.mlops.deployment.helpers import to_folder, replace_string_file
import re

logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)


def update_mlops_version_in_pipeline(folder_path: Path = Path(".")) -> None:
    """Update MLOps settings by overwriting the package version number.
    First, it will go through the pipeline definition and remove any quoatation mark prefix to akerbp.mlops
    (to make it robust against updating from previous versions),
    before it will replace the version number with whatever version the caller has on his/her local machine.

    Args:
        folder_path (Path, optional): Path to folder containing the pipeline file. Defaults to Path(".").
    """
    pipeline_file = Path("bitbucket-pipelines.yml")
    pipeline_path = folder_path / pipeline_file
    replacement_package = f"akerbp.mlops=={version}"
    pattern_package = re.compile("akerbp.mlops==.{5,}")
    replacement_version = f"Version {version}"
    pattern_version = re.compile("Version \S{5,}")
    pattern_prefix = re.compile('"akerbp')
    replacement_prefix = "akerbp"
    with pipeline_path.open() as f:
        pipeline = f.read()
        new_pipeline = re.sub(
            pattern_version,
            replacement_version,
            re.sub(
                pattern_package,
                replacement_package,
                re.sub(pattern_prefix, replacement_prefix, pipeline),
            ),
        )
    with pipeline_path.open("w") as f:
        f.write(new_pipeline)
    logger.info("MLOps version successfully updated in pipeline file")


def generate_pipeline(folder_path: Path = Path(".")) -> None:
    """Generate pipeline definition from template

    Args:
        folder_path (Path, optional): Path to folder that should contain the pipeline file. Defaults to Path(".").
    """
    pipeline_file = Path("bitbucket-pipelines.yml")
    pipeline_path = folder_path / pipeline_file
    pipeline = ("akerbp.mlops.deployment", pipeline_file)
    to_folder(pipeline, folder_path)
    replace_string_file("MLOPS_VERSION", version, pipeline_path)
    logger.info("Pipeline definition generated")


def setup_pipeline(folder_path: Path = Path(".")) -> None:
    """
    Set up pipeline file in the given folder.
    Update MLOps package version in the pipeline file if it exists, or generate from template if it doesn't.

    Args:
        folder_path (Path, optional): Path to folder that should contain the pipeline file. Defaults to Path(".").
    """
    pipeline_file = Path("bitbucket-pipelines.yml")
    pipeline_path = folder_path / pipeline_file
    if pipeline_path.exists():
        logger.info(f"Update MLOps version in pipeline definition to {version}")
        update_mlops_version_in_pipeline()
    else:
        logger.info("Generating pipeline definition from template")
        generate_pipeline()


if __name__ == "__main__":
    logging_config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name="akerbp.mlops.deployment.setup.py")
    logging.captureWarnings(True)

    setup_pipeline()
    if Path("mlops_settings.yaml").exists():
        logger.info("Validate settings file")
        validate_user_settings()
    else:
        logger.info("Create settings file template")
        generate_default_project_settings()
    logger.info("Done!")
