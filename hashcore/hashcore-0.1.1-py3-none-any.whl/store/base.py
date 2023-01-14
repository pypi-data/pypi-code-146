"""
Thie is the base module for the store package, it contains the Store Spec and HashStore class which must be extended by all store classes.
"""

import boto3
import pluggy
import os
import json

from hash import errors, utils
from hash import core

from google.cloud import storage
from google.api_core.exceptions import NotFound
from botocore.exceptions import ClientError

from hash.core import State
from hash import store_hookimpl

hookspec = pluggy.HookspecMarker("hash-store")


def store_init(func):
    def inner_init(self, config):
        self._init(config)
        return func(self, config)
    return inner_init


class StoreSpec:
    @hookspec
    def init(config):
        """Initilize the plugin."""

    @hookspec
    def store(state, resource_id):
        """Store the hash using id."""

    @hookspec
    def get(uid, _hash):
        """Get resource state by hash"""
    @hookspec
    def get_globals():
        """Get global data"""


class HashStore(object):
    """
    This is the base class for all store classes, it offers the re-usable methods which need to call other store backend
        specific methods to do their work, these methods include:

        store_artifacts: This method is calls the store_artifact for the chosen backend on all artifacts found in the state.
        get: This method class get_states to retrieve a list of all states for the current resource and return one of them
        based on the chosen hash
        store: This method calls store_state to store the current state of a resource, it reads all states from the backend, adds
        the new state, and then asks the backend to store the states again.
    """

    def _init(self, config):
        utils.check_type(config, dict, errors.ConfigStoreError,
                         False, f"config is required for {self.__class__}")
        organization = config.get("organization", None)
        if organization is None:
            raise errors.ConfigStoreError(
                f"organization key is required for every store config, not found in {config}")
        utils.check_type(organization, str, errors.ConfigStoreError, False,
                         f"organization should be string: found {type(organization)}")
        self.__org = organization
        project = config.get("project")
        if project is None:
            raise errors.ConfigStoreError(
                f"project key is required for every store config, not found in {config}")
        utils.check_type(project, str, errors.ConfigStoreError,
                         False, f"project should be string: found {type(project)}")
        self.__proj = project

    def get_organization(self):
        return self.__org

    def get_project(self):
        return self.__proj

    def store_artifacts(self, state: State):
        """
        This method is used to store all the artifacts of kind file found in the state.

        args:
            state (State): The state object which contains the artifacts that we want to save.

        return:
            Exception | NoneType: It returns an exception object if saving one artifact caused an error, and None otherwise
        """
        utils.check_type(state, State, errors.StateStoreError, False,
                         f"state must be State object: found {type(state)}")
        artifact_error = None
        artifacts = []
        for ac in core.all_actions:
            artifacts += state.get_result(ac).get("artifacts", [])
            for env in state.get_env_names(ac):
                artifacts += state.get_result(ac, env).get("artifacts", [])
        for artifact in artifacts:
            if artifact.getKind() == "file":
                try:
                    if artifact.isSaved():
                        continue
                    artifact.setSaved(True)
                    new_path = self.store_artifact(
                        artifact, state.get_resource_id())
                    # TODO: Get rid of this hack by making sure that the already saved artifacts are not processed here at all
                    if new_path != artifact.getData():
                        try:
                            os.remove(artifact.getData())
                        except Exception:
                            pass
                except Exception as e:
                    artifact_error = e
        return artifact_error

    def fix_artifacts(self, state, resource_id):
        envs_objects = state.get("envs", {})
        for env in envs_objects.keys():
            for ac in core.all_actions:
                artfs = envs_objects[env].get(ac, {}).get("artifacts", [])
                for artf in artfs:
                    if artf.get("kind") == "file":
                        with open(artf.get("data"), "wb") as f:
                            aft = utils.Artifact(
                                artf.get("id"),
                                artf.get("action"),
                                artf.get("env"),
                                artf.get("hash"),
                                artf.get("kind"),
                                artf.get("data"),
                                saved=True
                            )
                            f.write(self.read_artifact(aft, resource_id))
        no_env_artifacts = state.get("no_env", {}).get("artifacts", [])
        for artf in no_env_artifacts:
            for ac in core.all_actions:
                artfs = no_env_artifacts.get(ac, {}).get("artifacts", [])
                for art in artfs:
                    if art.get("kind") == "file":
                        with open(art.get("data"), "wb") as f:
                            aft = utils.Artifact(
                                art.get("id"),
                                art.get("action"),
                                art.get("env"),
                                art.get("hash"),
                                art.get("kind"),
                                art.get("data"),
                                saved=True
                            )
                            f.write(self.read_artifact(aft, resource_id))

    def get(self, resource_id: str, h: str):
        """
        This method is used to read a state from the backend.

        args:
            resource_id (str): The ID of resource that we want to read from its state.
            h (str): The hash of the state that we want to read.
        return:
            State: The state object
        """
        states = self.get_states(resource_id)
        if states is None or states == {}:
            return State(h, resource_id)
        state = states.get(h)
        if type(state) == str:
            state = json.loads(state)
        try:
            if state is not None and type(state) != State:
                state.get("hash")
        except AttributeError:
            print(state)
            raise errors.StateStoreError(
                f"Invalid state read from state store for resource {resource_id}, hash {h}")
        if state is not None:
            if type(state) == State:
                state = json.loads(state.get_json_str())
            self.fix_artifacts(state, resource_id)
        if state is None:
            st = State(h, resource_id)
        elif type(state) == dict:
            st = State.read_state(state, resource_id)
        elif type(state) == str:
            st = State.read_state(json.loads(state), resource_id)
        elif type(state) == State:
            st = state
        else:
            raise errors.ResourceStoreError(
                f"Got unkonwn state from state store for resource {resource_id} and hash {h}")
        return st

    def store(self, state: State):
        """
        This method is used to store a state in the backend.

        args:
            state (State): The state to store
        """
        utils.check_type(state, State, errors.StateStoreError, False,
                         f"state must be State object: found {type(state)}")
        resource_id = state.get_resource_id()
        states = self.get_states(resource_id)
        artifact_error = None
        globals = self.get_globals()
        glob = globals.get(resource_id)
        if not glob:
            globals[resource_id] = {}
        for ac in core.all_actions:
            for env in state.get_env_names(ac):
                if globals[resource_id].get(env):
                    if state.get_result(ac, env)._data().get("globals", {}) is None:
                        globals[resource_id][env][ac] = {
                            **globals[resource_id].get(ac, {})}
                    else:
                        globals[resource_id][env][ac] = {
                            **globals[resource_id].get(ac, {}), **state.get_result(ac, env)._data().get("globals", {})}
                else:
                    if state.get_result(ac, env)._data().get("globals", {}) is None:
                        globals[resource_id][env] = {
                            ac: {**globals[resource_id].get(ac, {})}
                        }
                    else:
                        globals[resource_id][env] = {
                            ac: {
                                **globals[resource_id].get(ac, {}), **state.get_result(ac, env)._data().get("globals", {})}
                        }
            if state.get_result(ac).get("globals", {}) is None:
                ac_globals = {}
            else:
                ac_globals = state.get_result(ac).get("globals", {})._data()
            if globals[resource_id].get("no_env"):
                globals[resource_id][ac] = {
                    **globals[resource_id].get(ac, {}), **ac_globals}
            else:
                globals[resource_id]["no_env"] = {
                    ac: {**globals[resource_id].get(ac, {}), **ac_globals}
                }
        self.store_globals(globals)
        artifact_error = self.store_artifacts(state)
        states[state.get_hash()] = state.get_json()
        self.store_state(json.dumps(
            states, cls=utils.HashJsonEncoder), resource_id)
        if artifact_error:
            raise artifact_error


class HashStoreLocalFile(HashStore):
    """
    This class is used to store resources in a local path.

    Required config key is output which is a directory path
    that must already exist.
    """
    @store_hookimpl
    @store_init
    def init(self, config):
        """
        Initialize the local file store, required key is **output**

        Args:
            config (dict): A dictionary with one key output which is the output path
                to store resources.
        """
        utils.check_type(config, dict, errors.ConfigStoreError, False,
                         f"Config must be a dictionary: found {type(config)}")
        try:
            output = config["output"]
        except KeyError:
            raise errors.ConfigStoreError(
                "output is required for Local File config")
        utils.check_type(output, str, errors.ConfigStoreError, False,
                         f"Output directory must be a string: found {type(output)}")
        if not os.path.exists(os.path.abspath(output)):
            raise errors.ConfigStoreError(f"Path {output} does not exist")
        self.__path = output
        # TODO: Check for absolute path
        if self.__path[0] != "/":
            self.__path = os.path.abspath(self.__path)
        self.__path = f"{self.__path}/{self.get_organization()}/{self.get_project()}"
        try:
            os.makedirs(self.__path)
        except FileExistsError:
            pass
        self.__state_file = "hash.json"
        self.__globals_file = "globals.json"

    @store_hookimpl
    def read_artifact(self, artifact, resource_id):
        path = os.path.join(self.__path, resource_id.replace(":", "/"))
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        path = os.path.join(path, artifact.file_name())
        with open(path, "rb") as f:
            return f.read()

    @store_hookimpl
    def store_artifact(self, artifact, resource_id):
        path = os.path.join(self.__path, resource_id.replace(":", "/"))
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        path = os.path.join(path, artifact.file_name())
        with open(artifact.getData(), "rb") as f:
            file_data = f.read()
        with open(path, "wb") as f:
            f.write(file_data)
        return path

    @store_hookimpl
    def get_states(self, resource_id):
        path = os.path.join(self.__path, resource_id.replace(":", "/"))
        states = {}
        if os.path.exists(os.path.join(path, self.__state_file)):
            with open(os.path.join(path, self.__state_file), "r+") as f:
                try:
                    states = json.load(f)
                    return states
                except json.decoder.JSONDecodeError as e:
                    pass
        return states

    @store_hookimpl
    def store_globals(self, _globals: dict):
        global_path = os.path.join(self.__path, self.__globals_file)
        with open(global_path, "w+") as f:
            json.dump(_globals, f)

    @store_hookimpl
    def store_state(self, states: dict, resource_id: str):
        path = os.path.join(self.__path, resource_id.replace(":", "/"))
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        with open(os.path.join(path, self.__state_file), "w") as f:
            f.write(states)

    @store_hookimpl
    def get_globals(self):
        global_path = os.path.join(self.__path, self.__globals_file)
        data = {}
        try:
            with open(global_path, "r") as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError:
                    pass
        except FileNotFoundError:
            pass
        return data


class HashStoreDOSpace(HashStore):
    @store_hookimpl
    @store_init
    def init(self, config):
        try:
            space_name = config["space_name"]
            region_name = config["region_name"]
        except KeyError:
            raise ValueError(
                f"space_name and region_name are required for {self.__class__}")
        session = boto3.session.Session()
        self._space_name = space_name
        self._client = session.client('s3',
                                      region_name=region_name,
                                      endpoint_url=f'https://{region_name}.digitaloceanspaces.com',
                                      aws_access_key_id=os.getenv(
                                          'SPACES_KEY'),
                                      aws_secret_access_key=os.getenv('SPACES_SECRET'))
        buckets = self._client.list_buckets()
        for bucket in buckets["Buckets"]:
            if bucket["Name"] == space_name:
                return
        raise errors.StoreNotFound(
            f"No space with name {space_name} found in region {region_name}")

    @store_hookimpl
    def read_artifact(self, artifact, resource_id):
        key = f"{self.get_organization()}-{self.get_project()}-{resource_id}-{artifact.file_name()}"
        try:
            data = self._client.get_object(Bucket=self._space_name,
                                           Key=key
                                           )
            return data["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] != "NoSuchKey":
                raise errors.StoreError(e)

    @store_hookimpl
    def store_artifact(self, artifact, resource_id: str):
        key = f"{self.get_organization()}-{self.get_project()}-{resource_id}-{artifact.file_name()}"
        with open(artifact.getData(), "rb") as f:
            data = f.read()
        self._client.put_object(Bucket=self._space_name,
                                Key=key,
                                Body=data,
                                ACL="private"
                                )

    @store_hookimpl
    def get_states(self, uid: str):
        key = f"{self.get_organization()}-{self.get_project()}-{uid}-hash.json"
        data = {}
        try:
            data = self._client.get_object(Bucket=self._space_name,
                                           Key=key
                                           )
            return json.loads(data["Body"].read())
        except ClientError as e:
            if e.response["Error"]["Code"] != "NoSuchKey":
                raise errors.StoreError(e)
        return data

    @store_hookimpl
    def store_state(self, data: list, uid: str):
        key = f"{self.get_organization()}-{self.get_project()}-{uid}-hash.json"
        self._client.put_object(Bucket=self._space_name,
                                Key=key,
                                Body=bytes(data, "utf8"),
                                ACL="private"
                                )

    @store_hookimpl
    def get_globals(self):
        globals_key = f"{self.get_organization()}-{self.get_project()}-globals.json"
        data = {}
        try:
            data = self._client.get_object(Bucket=self._space_name,
                                           Key=globals_key
                                           )
            return json.loads(data["Body"].read())
        except ClientError as e:
            if e.response["Error"]["Code"] != "NoSuchKey":
                raise errors.StoreError(e)
        return data

    @store_hookimpl
    def store_globals(self, _globals: dict):
        globals_key = f"{self.get_organization()}-{self.get_project()}-globals.json"
        self._client.put_object(Bucket=self._space_name,
                                Key=globals_key,
                                Body=bytes(json.dumps(globals), "utf8"),
                                ACL="private"
                                )


class HashStoreGCPBucket(HashStore):
    def __init__(self) -> None:
        self.client = None
        self.bucket = None

    @store_hookimpl
    @store_init
    def init(self, config):
        try:
            bucket_name = config["bucket"]
            project_name = config["project_name"]
        except KeyError:
            raise errors.ConfigStoreError(
                "bucket and project_name keys are required for GCP bucket backends")
        self.client = storage.Client(project_name)
        try:
            self.bucket = self.client.get_bucket(bucket_name)
        except NotFound:
            raise errors.ConfigStoreError(
                f"Bucket with name {bucket_name} does not exist or you have no permission on it")

    def get_states(self, resource_id: str) -> list:
        key = f"{self.get_organization()}-{self.get_project()}-{resource_id}-hash.json"
        blob = storage.Blob(key, self.bucket)
        try:
            return json.loads(blob.download_as_text())
        except NotFound:
            return {}

    def store_state(self, states: str, resource_id: str):
        key = f"{self.get_organization()}-{self.get_project()}-{resource_id}-hash.json"
        blob = storage.Blob(key, self.bucket)
        blob.upload_from_string(states)

    def get_globals(self):
        key = f"{self.get_organization()}-{self.get_project()}-globals.json"
        blob = storage.Blob(key, self.bucket)
        try:
            return json.loads(blob.download_as_text())
        except NotFound:
            return {}

    def store_globals(self, _globals: dict):
        key = f"{self.get_organization()}-{self.get_project()}-globals.json"
        blob = storage.Blob(key, self.bucket)
        blob.upload_from_string(json.dumps(_globals))

    def store_artifact(self, artifact, uid):
        key = f"{self.get_organization()}-{self.get_project()}-{uid}-{artifact.file_name()}"
        blob = storage.Blob(key, self.bucket)
        blob.upload_from_filename(artifact.getData())

    def read_artifact(self, artifact, resource_id):
        key = f"{self.get_organization()}-{self.get_project()}-{resource_id}-{artifact.file_name()}"
        blob = storage.Blob(key, self.bucket)
        try:
            return blob.download_as_bytes()
        except NotFound:
            raise errors.StoreError(
                f"Artifact with id {artifact.getId()} not found in state for resource {resource_id}")


def get_plugin_manager():
    """
    Return the plugin manager for hash-store plugins.
    """
    pm = pluggy.PluginManager("hash-store")
    pm.add_hookspecs(StoreSpec)
    pm.load_setuptools_entrypoints("hash-store")
    pm.register(HashStoreLocalFile(), "LocalFile")
    pm.register(HashStoreDOSpace(), "DOSpace")
    pm.register(HashStoreGCPBucket(), "GCPBucket")
    return pm


def get_store(store, args):
    """
    Return a store plugin by its name

    Args:
        store (str): The name of the store to return.
        args (dict): A dictionary which contains the options for this store

    Return:
        object: The store object, which can be used to store, list and get resources.
    """
    pm = get_plugin_manager()
    plugins = pm.list_name_plugin()
    for plugin in plugins:
        if store == plugin[0]:
            hash_store = plugin[1]
            hash_store.init(args)
            return hash_store
    raise errors.StoreNotFound("No store with name ", store)
