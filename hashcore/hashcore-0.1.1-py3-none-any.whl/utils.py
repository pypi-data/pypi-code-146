from datetime import datetime
import json
import yaml
import traceback
import subprocess
from hash import errors

import os
import jinja2


class Artifact:
    """
    This class is used to store stage's results such as files, URls, ect ....
    """
    __kinds = ["file", "url", "text"]

    def __init__(self, aft_id: str, action: str, env: str, hash: str, kind: str,  data, relative_path="", file_data=None, saved=False) -> None:
        if aft_id is None:
            raise errors.ArtifactError("No id found for artifact")
        check_type(aft_id, str, errors.ArtifactError, False,
                   f"aft_id should be string: found {type(aft_id)}")
        if action is None:
            raise errors.ArtifactError("Action is not found")
        check_type(action, str, errors.ArtifactError, False,
                   f"action should be string: found {type(action)}")
        check_type(env, str, errors.ArtifactError, True,
                   f"env should be string: found {type(env)}")
        if hash is None:
            raise errors.ArtifactError("Hash is not found in artifact")
        check_type(hash, str, errors.ArtifactError, True,
                   f"hash should be string: found {type(hash)}")
        if kind is None or kind not in self.__kinds:
            raise errors.ArtifactError(
                "kind is not found or not acceptible in artifact")
        check_type(kind, str, errors.ArtifactError, True,
                   f"kind should be string: found {type(kind)}")
        if data is None:
            raise errors.ArtifactError(f"data is not found in artifact")
        check_type(data, str, errors.ArtifactError, True,
                   f"data should be string: found {type(data)}")
        self.__id = aft_id
        self.__action = action
        self.__env = env
        self.__hash = hash
        self.__kind = kind
        self.__saved = saved
        self.__data = str(data)
        self.__relative_path = relative_path
        if self.__kind == "file":
            if file_data is None:
                with open(self.__data, "rb") as f:
                    pass
            else:
                with open(self.__data, "wb") as f:
                    f.write(file_data)

    def getId(self):
        return self.__id

    def getAction(self):
        return self.__action

    def getEnv(self):
        return self.__env

    def getKind(self):
        return self.__kind

    def getHash(self):
        return self.__hash

    def file_name(self):
        return f"artifact-{self.__id}-{self.__action}-{self.__env}-{self.__hash}"

    def getData(self):
        return self.__data

    def setRelativePath(self, data):
        self.__relative_path = data

    def isSaved(self):
        return self.__saved

    def setSaved(self, saved):
        self.__saved = saved

    def getDict(self):
        return {
            "id": self.__id,
            "action": self.__action,
            "env": self.__env,
            "hash": self.__hash,
            "kind": self.__kind,
            "data": self.__data,
            "saved": self.__saved,
            "relative_path": self.__relative_path
        }

    def __repr__(self) -> str:
        return f"<Artifact: id {self.__id} action {self.__action} env {self.__env} data {self.__data}>"

    def __eq__(self, art) -> bool:
        return self.getId() == art.getId() and self.getAction() == art.getAction() and self.getEnv() == art.getEnv() and self.getKind() == art.getKind() and self.getHash() == art.getHash() and self.getData() == art.getData()

    @classmethod
    def read_artifact(cls, artifact_data: dict):
        return cls(artifact_data.get("id"), artifact_data.get("action"), artifact_data.get("env"), artifact_data.get("hash"), artifact_data.get("kind"), artifact_data.get("data"), artifact_data.get("relative_path", ""), artifact_data.get("file_data"), saved=artifact_data.get("saved", False))


class Globals(object):
    def __init__(self, globals: dict, env: dict, dry: bool) -> None:
        self.globals = globals
        self.env = env
        self.dry = dry
        self.deps = []

    def get(self, id: str, action: str, name: str, env=None):
        if self.dry:
            d = {
                "id": id,
                "action2": action
            }
            self.deps.append(d)
            return {}
        if env is None:
            if self.env:
                return self.globals.get(id, {}).get(self.env, {}).get(action, {}).get(name)
            else:
                return self.globals.get(id, {}).get("no_env", {}).get(action, {}).get(name)
        else:
            return self.globals.get(id, {}).get(env, {}).get(action, {}).get(name)

    def __repr__(self) -> str:
        return f"<Globlas: {self.globals}>"


class Artifacts(object):
    def __init__(self, dry: bool, func) -> None:
        self.dry = dry
        self.func = func
        self.deps = []

    def get_artifact(self, id: str, action: str, name: str):
        if self.dry:
            d = {
                "id": id,
                "action2": action
            }
            self.deps.append(d)
            return Artifact("", "", "", "", "text", "test")
        return self.func(id, action, name)


class SilentUndefined(jinja2.Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''


class Template:
    """
    This class is used to render all templates in a resource
    """

    def __init__(self, path: str, silent_undefined=False) -> None:
        if not os.path.exists(path):
            raise errors.TemplatePathNotFoundError(f"Path {path} not found")
        if silent_undefined:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(path), undefined=SilentUndefined)
        else:
            self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        self.path = path

    def template(self, file: str, **config) -> None:
        try:
            tmp = self.env.get_template(file)
            return tmp.render(config)
        except jinja2.exceptions.TemplateNotFound as e:
            raise errors.TemplateRenderError(
                "file not found " + str(e) + " in path " + self.path)
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise errors.TemplateRenderError(str(e))


def check_type(var, t, e, allow_none, msg):
    if allow_none:
        if var is not None and type(var) != t:
            raise e(msg)
    else:
        if type(var) != t:
            raise e(msg)


def check_action_env(a, e):
    check_type(a, str, errors.StateError, False,
               f"Action must be str, found {type(a)}")
    check_type(e, str, errors.StateError, True,
               f"Env must be str, found {type(e)}")


def check_action_env_result(a, e, r):
    check_action_env(a, e)
    check_type(r, dict, errors.StateError, False,
               f"Result must be dict, found {type(a)}")


def check_action(a):
    check_type(a, str, errors.ActionError, False,
               f"Action must be str, found {type(a)}")


class HashJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        if isinstance(obj, Artifact):
            return obj.getDict()
        if isinstance(obj, ImDict):
            return obj._data()
        return json.JSONEncoder.default(self, obj)


class ImDict(object):
    """
    This class represents an immutable version of a dictionary, it only allows reads but no writes
    """

    def __init__(self, data: dict) -> None:
        if type(data) != dict:
            raise errors.DictError(
                f"Expected argument of type dict: found {type(data)}")
        self.__data = data

    def __getitem__(self, key):
        item = self.__data[key]
        if type(item) == dict:
            return ImDict(item)
        if type(item) == list:
            return tuple(item)
        return item

    def __setitem__(self, key, data):
        raise errors.DictError("You cannot change values in this dictionary")

    def get(self, key, default=None):
        item = self.__data.get(key, default)
        if type(item) == dict:
            return ImDict(item)
        if type(item) == list:
            return tuple(item)
        return item

    def _data(self):
        cs = traceback.extract_stack()
        if len(cs) < 2:
            return {}
        if cs[-2].name != "default" and cs[-2].name != "store":
            return {}
        return self.__data

    def __eq__(self, __o: object) -> bool:
        return self.__data == __o.__data

    def __len__(self):
        return len(self.__data)

    def __str__(self) -> str:
        return str(self.__data)

    def keys(self) -> list:
        return self.__data.keys()

    def items(self) -> list:
        return self.__data.items()


def parse_resource_file(file: str) -> dict:
    """
    Read a resource file and return a parsed dictionary.

    args:
        file (str): The path to the resource's file

    return:
        dict: A dictionary of the resource's file
    """
    check_type(file, str, FileNotFoundError, False,
               f"{file} is not a file path or cannot be found")
    with open(file, "r") as f:
        try:
            data = yaml.safe_load(f)
            check_type(data, dict, errors.ResourceError, False,
                       f"resource file must be a yaml file: {file}")
        except yaml.scanner.ScannerError as e:
            raise errors.ResourceInvalidYaml(str(e))
        except yaml.constructor.ConstructorError as e:
            raise errors.ResourceInvalidYaml(str(e))
    if data.get("kind") is None:
        raise errors.ResourceError(f"Found no kind in resource file at {file}")
    metadata = data.get("metadata")
    if metadata is None:
        raise errors.ResourceError(
            f"Found no metadata in resource file at {file}")
    if type(metadata) != dict:
        raise errors.ResourceError(
            f"Metadata must be dict found {type(metadata)} in resource file at {file}")
    if metadata.get("name") is None:
        raise errors.ResourceError(
            f"Name not found in metadata of resource file at {file}")
    return data


class Script(object):
    """
    This class is used to define a script that can be executed and use
    its output, it is used for executing action overrides in resources
    """

    def __init__(self, script_path: str = "") -> None:
        if script_path != "":
            check_type(script_path, str, errors.ScriptError, False,
                       f"Script path must be string: failed {type(script_path)}")
            if not os.path.isfile(script_path) or not os.access(script_path, os.X_OK):
                raise errors.ScriptNotFoundError(
                    f"Cannot find script in path {script_path} or it is not executable")
            self.__script_path = script_path

    def run(self, path: str) -> subprocess.CompletedProcess:
        return subprocess.run(self.__script_path, capture_output=True, cwd=path, check=True)

    def execute(self, command: str, path: str) -> subprocess.CompletedProcess:
        return subprocess.run(command, cwd=path, check=True, capture_output=True, shell=True)
