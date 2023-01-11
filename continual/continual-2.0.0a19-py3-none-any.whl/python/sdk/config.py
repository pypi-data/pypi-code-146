import os
from pathlib import Path
import yaml
from typing import Optional, List
from omegaconf import OmegaConf
from dataclasses import dataclass


@dataclass
class ContinualConfig:
    endpoint: Optional[str] = None
    email: Optional[str] = None
    api_key: Optional[str] = None
    project: Optional[str] = None
    environment: Optional[str] = None
    style: Optional[str] = None
    raise_exception: Optional[bool] = False
    debug: Optional[bool] = False


class Config:
    """Config for client.

    Reads configuration, in listed order, from:
        * Files:
            * ~/.continual/continual.config
            * ./continual.config
            * ./.continual.config
            * `CONTINUAL_CONFIG` file location from environment variable, if set
        * Environment variables:
            * `CONTINUAL_CONFIG`
            * `CONTINUAL_API_KEY`
            * `CONTINUAL_PROJECT`
            * `CONTINUAL_ENVIRONMENT`
            * `CONTINUAL_ENDPOINT`
            * `CONTINUAL_STYLE`
            * `CONTINUAL_RAISE_EXCEPTION`
            * `CONTINUAL_DEBUG`
        * Config __init__ params (`Config(project=)`)
        * Config setters (`config.project=`), setter methods (`config.set_project()`)
    """

    _endpoint: str = ""

    _email: str = ""

    _api_key: str = ""

    _project: str = ""

    _environment: str = ""

    _style: str = ""

    _raise_exception: bool = False

    _debug: bool = False

    _app_url: str = ""

    _config_file_paths: List[str] = []

    def __init__(
        self,
        api_key: Optional[str] = None,
        email: Optional[str] = None,
        project: Optional[str] = None,
        environment: Optional[str] = None,
        endpoint: Optional[str] = None,
        style: Optional[str] = None,
        raise_exception: Optional[bool] = False,
        debug: Optional[bool] = False,
    ) -> None:
        """Initialize config.

        Args:
            api_key: API key.
            email: Email address.
            project: Current project.
            environment: Current environment.
            endpoint: Cluster endpoint.
            style: Continual style.
            raise_exception: Raise exception if an error occurs.
            debug: Print stack traces and other debug information
        """

        configs = []
        file_config_paths = []

        default_config = OmegaConf.structured(
            ContinualConfig(
                endpoint="https://sdk.continual.ai",
                email=None,
                api_key=None,
                project=None,
                environment=None,
                style="GREEN",  # cli/utils/ContinualStyle.GREEN
                raise_exception=False,
                debug=False,
            )
        )
        configs.append(default_config)

        home_config_path = os.path.join(Path.home(), ".continual", "continual.yaml")
        if os.path.exists(home_config_path):
            file_config_paths.append(home_config_path)
            try:
                home_config = OmegaConf.load(home_config_path)
                configs.append(home_config)
            except Exception as e:
                print(e)

        working_dir_config_path = os.path.join(os.getcwd(), "continual.yaml")
        if os.path.exists(working_dir_config_path):
            file_config_paths.append(working_dir_config_path)
            try:
                working_dir_config = OmegaConf.load(working_dir_config_path)
                configs.append(working_dir_config)
            except Exception as e:
                print(e)

        working_dir_config_path_2 = os.path.join(os.getcwd(), ".continual.yaml")
        if os.path.exists(working_dir_config_path_2):
            file_config_paths.append(working_dir_config_path_2)
            try:
                working_dir_config_2 = OmegaConf.load(working_dir_config_path_2)
                configs.append(working_dir_config_2)
            except Exception as e:
                print(e)

        if os.environ.get("CONTINUAL_CONFIG"):
            config_file_path = os.environ.get("CONTINUAL_CONFIG")
            if os.path.exists(config_file_path):
                file_config_paths.append(config_file_path)
                try:
                    file_config = OmegaConf.load(config_file_path)
                    configs.append(file_config)
                except Exception as e:
                    print(e)

        OMEGACONF_MISSING = "???"

        env_config = OmegaConf.structured(
            ContinualConfig(
                endpoint=os.environ.get("CONTINUAL_ENDPOINT", OMEGACONF_MISSING),
                email=OMEGACONF_MISSING,
                api_key=os.environ.get("CONTINUAL_API_KEY", OMEGACONF_MISSING),
                project=os.environ.get("CONTINUAL_PROJECT", OMEGACONF_MISSING),
                environment=os.environ.get("CONTINUAL_ENVIRONMENT", OMEGACONF_MISSING),
                style=os.environ.get("CONTINUAL_STYLE", OMEGACONF_MISSING),
                raise_exception=os.environ.get(
                    "CONTINUAL_RAISE_EXCEPTION", OMEGACONF_MISSING
                ),
                debug=os.environ.get("CONTINUAL_DEBUG", OMEGACONF_MISSING),
            )
        )
        configs.append(env_config)

        params_config = OmegaConf.structured(
            ContinualConfig(
                endpoint=endpoint if endpoint else OMEGACONF_MISSING,
                email=email if email else OMEGACONF_MISSING,
                api_key=api_key if api_key else OMEGACONF_MISSING,
                project=project if project else OMEGACONF_MISSING,
                environment=environment if environment else OMEGACONF_MISSING,
                style=style if style else OMEGACONF_MISSING,
                raise_exception=raise_exception
                if raise_exception
                else OMEGACONF_MISSING,
                debug=debug if debug else OMEGACONF_MISSING,
            )
        )
        configs.append(params_config)

        conf = OmegaConf.merge(*configs)

        self._endpoint = conf.endpoint
        self.set_api_key(conf.api_key, False)
        self._email = conf.email
        self.set_project(conf.project, False)
        self.set_environment(conf.environment, False)
        self._style = conf.style
        self._raise_exception = conf.raise_exception
        self._debug = conf.debug
        self._config_file_paths = file_config_paths
        self._app_url = self._get_app_url(self.endpoint)

    @property
    def endpoint(self) -> str:
        """Continual endpoint."""
        return self._endpoint

    @property
    def email(self) -> str:
        """Email address."""
        return self._email

    @property
    def api_key(self) -> str:
        """API key."""
        return self._api_key

    @property
    def project(self) -> str:
        """Default project."""
        return self._project

    @property
    def environment(self) -> str:
        """Default environment."""
        return self._environment

    @property
    def style(self) -> str:
        """Default template style"""
        return self._style

    @property
    def raise_exception(self) -> bool:
        """Raise exception if an error occurs"""
        return self._raise_exception

    @property
    def debug(self) -> bool:
        """Print stack traces and other debug information"""
        return self._debug

    def set_project(self, project: str, save: bool = True) -> str:
        """Set the config project.

        Arguments:
            project: The id or name of the project to use in this config
            save: Whether or not to save this configuration to disk.

        Returns:
            The formatted project name set on config
        """
        if project and "/" not in project:
            project = "projects/" + project

        self._project = project

        if save:
            self.save()

        return self.project

    def set_api_key(self, api_key: str, save: bool = True) -> str:
        """Set the API key.

        Arguments:
            api_key: The API key to use in this config
            save: Whether or not to save this configuration to disk.

        Returns:
            The formatted API key set on config
        """

        self._api_key = api_key

        if save:
            self.save()

        return self.api_key

    def set_environment(self, environment: str, save: bool = True) -> str:
        """Set the environment.

        Arguments:
            environment: The environment to use in this config
            save: Whether or not to save this configuration to disk.

        Returns:
            The formatted environment set on config
        """

        if environment:
            if "/" in environment:
                splits = environment.split("/")
                if len(splits) == 4:
                    self._project = "/".join(splits[:-2])
            self._environment = environment
            if save:
                self.save()
        return self.environment

    def show(self):
        """Print config information."""
        print(f"Config Files:")
        if len(self._config_file_paths) > 0:
            print("\n".join(map(lambda x: f"  {x}", self._config_file_paths)))
        print(f"Email: {self.email or ''}")
        print(f"Endpoint: {self.endpoint or ''}")
        print(f"Project: {self.project or ''}")
        print(f"Environment: {self.environment or ''}")
        print(f"Style: {self.style or ''}")
        print(f"Raise Exception: {self.raise_exception or ''}")
        print(f"Debug: {self.debug or ''}")
        print(f"API Key: {'*' * len(self.api_key) if self.api_key else ''}")

    def save(self):
        """Save config to config file."""

        # TODO: perhaps allow specifying where to save (global/homedir vs local/workingdir)

        if os.environ.get("CONTINUAL_CONFIG"):
            config_file_path = os.environ.get("CONTINUAL_CONFIG")
            if os.path.exists(config_file_path):
                Path(os.path.dirname(config_file_path)).mkdir(
                    parents=True, exist_ok=True
                )
                with open(config_file_path, "w") as outfile:
                    # TODO: consider warning, or not saving, api_key here (since it's a secret)
                    config = dict(
                        email=self.email,
                        api_key=self.api_key,
                        project=self.project,
                        environment=self.environment,
                        endpoint=self.endpoint,
                        style=self.style,
                        raise_exception=self.raise_exception,
                        debug=self.debug,
                    )
                    yaml.dump(config, outfile)
        else:
            with open(os.path.join(os.getcwd(), "continual.yaml"), "w") as outfile:
                config = dict(
                    project=self.project,
                    endpoint=self.endpoint,
                    style=self.style,
                    raise_exception=self.raise_exception,
                    debug=self.debug,
                )
                yaml.dump(config, outfile)
            with open(os.path.join(os.getcwd(), ".continual.yaml"), "w") as outfile:
                config = dict(
                    email=self.email,
                    api_key=self.api_key,
                    environment=self.environment,
                )
                yaml.dump(config, outfile)
                # TODO: consider ensuring that .continual.yaml is git ignored

    def _get_app_url(self, client_endpoint: str):
        app_url = "https://app.continual.ai"
        if (
            "localhost" in client_endpoint.lower()
            or "host.docker.internal" in client_endpoint.lower()
            or "ngrok.io" in client_endpoint.lower()
        ):
            app_url = "http://localhost:8111"
        return app_url
