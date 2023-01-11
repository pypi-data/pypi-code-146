import logging
import os
import shutil

import click
import yaml


class CopyDefaultConfigs:

    def __init__(self, config_output_dir: str, default_config_dir: str):
        self.config_output_dir = config_output_dir
        self.default_config_dir = default_config_dir
        self.logger = logging.getLogger(__name__)

    def merge(self):
        for dir_path, _, file_names in os.walk(self.default_config_dir):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                relative_path = os.path.relpath(
                    file_path, self.default_config_dir
                )
                output_path = os.path.join(
                    self.config_output_dir, relative_path
                )
                self.logger.debug(
                    f"Processing file: {file_path}. Output path: {output_path}"
                )
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copyfile(file_path, output_path)
                os.chmod(output_path, 0o644)


class OverrideNonYamlConfigs:
    """Copy overridden configuration files from override directory
    to the destination directory. This kind of override should be used
    very sparingly as deployed changes in the container would be ignored
    and the entire file will be replaced.

    Override directory is considered flattened to avoid mistakes. This
    makes an assumption that we don't have multiple config files with same name.

    config.default/pip/pip.config
    config.default/bar.ini
    
    config.override/pip.config
    config.override/foo.ini
    
    After running merge this will generate:

    config/pip/pip.config [overridden]
    config/bar.ini [default]
    NOTE: foo.ini is skipped as it is not present in config.default.
    """

    def __init__(
        self, override_dir: str, config_output_dir: str, default_config_dir: str
    ) -> None:
        self.override_dir = override_dir
        self.config_output_dir = config_output_dir
        self.default_config_dir = default_config_dir
        self.logger = logging.getLogger(__name__)

    def merge(self):
        if not os.path.isdir(self.override_dir):
            if os.path.isfile(self.override_dir):
                raise ValueError(
                    "Expected a directory but found a file at " +
                    self.override_dir
                )
            self.logger.info(
                "Did not find override directory [%s], skipping non yaml file merge.",
                self.override_dir
            )
            return
        override_files = {
            f for f in os.listdir(self.override_dir)
            if os.path.isfile(os.path.join(self.override_dir, f))
        }

        directories_in_override = {
            f for f in os.listdir(self.override_dir)
            if os.path.isdir(os.path.join(self.override_dir, f))
        }

        if len(directories_in_override) != 0:
            raise ValueError(
                "Override directory should only have files, found directories: "
                + str(directories_in_override)
            )

        for key in override_files:
            name, file_extension = os.path.splitext(key)
            if file_extension.lower() in [".yaml", ".yml"
                                         ] and not name.startswith("override"):
                raise click.BadParameter(
                    "Override directory has YAML file. YAMLs should be overridden using override.yaml instead. Path: "
                    + key
                )

        override_files = {
            f for f in override_files
            if os.path.splitext(f)[1].lower() not in [".yaml", ".yml"]
        }
        # we will only override files that are a part of default_config_dir
        for dir_path, _, file_names in os.walk(self.default_config_dir):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                relative_path = os.path.relpath(
                    file_path, self.default_config_dir
                )
                output_path = os.path.join(
                    self.config_output_dir, relative_path
                )
                self.logger.debug(
                    f"Processing file: {file_path}. Output path: {output_path}"
                )

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                if file_name in override_files:
                    override_file = os.path.join(self.override_dir, file_name)
                    self.logger.info(
                        f"Overriding entire content of {file_path} by content of {override_file}"
                    )
                    shutil.copyfile(override_file, output_path)
                    os.chmod(output_path, 0o644)


class MergeDictionaryConfiguration:
    PRIMITIVE_TYPES = (int, str, bool, float)
    STR_TYPES = (str)
    LIST_TYPES = (list, tuple)

    @classmethod
    def subst_merge(cls, default, override, logger=None):
        """Merge dictionaries but substitute array."""
        if logger is None:
            logger = logging.getLogger(__name__)
        logger.debug('Merging %s and %s' % (default, override))
        # TODO(AU): should we override with None here?
        if override is None:
            logger.debug('Skip as override is None')

        # Primitive types are just substituted.
        # Lists are also substituted as merging lists is non-trivial.
        if default is None or isinstance(
            override, cls.PRIMITIVE_TYPES
        ) or isinstance(override, cls.LIST_TYPES):
            logger.debug(
                'Replace default "%s"  with override "%s"', default, override
            )
            default = override
        elif isinstance(default, dict):
            if not isinstance(override, dict):
                raise ValueError(
                    'Cannot merge %s to %s (occurred when merging "%s" and "%s")',
                    type(override), type(default), default, override
                )
            logger.debug('Merging dicts "%s" and "%s"', default, override)
            # Take the keys from default dictionary, if it is not in override, keep it.
            # If it is in override the merge the values recursively.
            # Add additional keys from override as is.
            for k in override:
                if k in default:
                    logger.debug(
                        'Merging dicts: both in override and default. Key "%s": "%s" and "%s"',
                        k, default[k], override[k]
                    )
                    default[k] = MergeDictionaryConfiguration.subst_merge(
                        default[k], override[k]
                    )
                else:
                    logger.debug('Merging dicts: only in override. Key "%s"', k)
                    default[k] = override[k]
        logger.debug('Merge outcome: "%s"', default)
        return default


class MergeYamlConfiguration:
    """Merge YAML configuration with an override file.
    NOTE: List values will be substituted and not merged.
    Sample override file:
    ```
    aiq_config.yaml:
        user_data_reader:
            keep_default_na: true
    coordinator-config.yaml:
        portStartRange: 16000
        portEndRange: 17000
    ```
    """

    def __init__(
        self, override_file: str, config_output_dir: str,
        default_config_dir: str
    ) -> None:
        self.override_file = override_file
        self.config_output_dir = config_output_dir
        self.default_config_dir = default_config_dir
        self.logger = logging.getLogger(__name__)

    def merge(self) -> None:
        overrides = dict()
        if os.path.isfile(self.override_file):
            self.logger.info(f"Reading override file from {self.override_file}")
            with open(self.override_file) as override_fd:
                overrides = yaml.safe_load(override_fd)
        else:
            self.logger.warning(
                f"Override file does not exist: {self.override_file}"
            )

        for key in overrides:
            _, file_extension = os.path.splitext(key)
            if file_extension.lower() not in [".yaml", ".yml"]:
                raise click.BadParameter(
                    "Override provided for non-YAML file. This is not currently supported. Path: "
                    + key
                )

        self.logger.info(f"Overrides available: {overrides.keys()}")

        applied_overrides = set()
        for dir_path, _, file_names in os.walk(self.default_config_dir):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                relative_path = os.path.relpath(
                    file_path, self.default_config_dir
                )
                output_path = os.path.join(
                    self.config_output_dir, relative_path
                )
                self.logger.debug(
                    f"Processing file: {file_path}. Output path: {output_path}"
                )

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                if file_name in overrides:
                    applied_overrides.add(file_name)
                    self.logger.info(
                        f"Found override for {file_name}, performing a merge"
                    )
                    merged = self._merge_configs(
                        overrides[file_name], file_path
                    )
                    with open(output_path, "w") as output_fd:
                        self.logger.info(
                            "Merge output: [writing to file %s]: \n%s",
                            output_path, merged
                        )
                        yaml.safe_dump(merged, output_fd)
                    os.chmod(output_path, 0o644)
                else:
                    self.logger.debug(f"No override found for {relative_path}")
        overrides_not_applied = set(overrides.keys()
                                   ).difference(applied_overrides)
        if overrides_not_applied:
            raise ValueError(
                (
                    f"Additional sections found in overrides file that did"
                    f" not match any default config: {overrides_not_applied}."
                    f" Ensure there are no typos or remove the override."
                )
            )

    def _merge_configs(self, override_dict, default_file) -> dict():
        with open(default_file) as default_file_fd:
            default_conf = yaml.safe_load(default_file_fd)
            conf = MergeDictionaryConfiguration.subst_merge(
                default_conf, override_dict, logger=self.logger
            )
            return conf


@click.group()
def config():
    pass


@config.command()
@click.option("--override_file", required=True, type=click.Path(file_okay=True))
@click.option("--override_dir", required=True, type=click.Path(dir_okay=True))
@click.option(
    "--config_output_dir",
    required=True,
    type=click.Path(dir_okay=True, writable=True)
)
@click.option(
    "--default_config_dir", required=True, type=click.Path(exists=True)
)
@click.option('--verbose', is_flag=True)
def merge(
    override_file, override_dir, config_output_dir, default_config_dir, verbose
):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    copy_default_config_tool = CopyDefaultConfigs(
        click.format_filename(config_output_dir),
        click.format_filename(default_config_dir)
    )
    copy_default_config_tool.merge()

    non_yaml_override_tool = OverrideNonYamlConfigs(
        click.format_filename(override_dir),
        click.format_filename(config_output_dir),
        click.format_filename(default_config_dir)
    )
    non_yaml_override_tool.merge()

    yaml_merge_tool = MergeYamlConfiguration(
        click.format_filename(override_file),
        click.format_filename(config_output_dir),
        click.format_filename(default_config_dir)
    )
    yaml_merge_tool.merge()


if __name__ == '__main__':
    config()
