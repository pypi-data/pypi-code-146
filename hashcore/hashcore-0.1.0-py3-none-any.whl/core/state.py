"""
State module defines State class with all the methods, functions needed to manage state, it ensures
that the internal state structure is hidden from consumers of the module and that only methods
are used to manipulate or read state.
"""

from datetime import datetime
import json

from hash import errors, utils

all_actions = ["build", "test", "publish", "deploy"]
globals_key = "globals"
artifacts_key = "artifacts"


class State(object):
    """
    This class defines a single state for a single resource, hash and resource ID combination make the
    state unique.
    """

    def __init__(self, _hash: str, resource_id: str) -> None:
        if type(_hash) != str:
            raise errors.StateError(f"hash must be string not {type(_hash)}")
        if type(resource_id) != str:
            raise errors.StateError(
                f"resource id must be string not {type(resource_id)}")
        self.__hash = _hash
        self.__resource_id = resource_id
        self.__envs = {}
        self.__no_env = {}
        self.__status = {
            "last_action": "",
            "error": ""
        }
        self.__deps = {}
        self.__vcs = {}
        self.__updated_at = datetime.now()

    def __check_result_artifacts(self, result: dict, action: str, env=None):
        artifacts = result.get(artifacts_key)
        if artifacts is None:
            return
        utils.check_type(artifacts, list, errors.StateArtifactError,
                         False, f"Artifacts must be a list: found {type(artifacts)}")
        for index in range(len(artifacts)):
            if type(artifacts[index]) == dict:
                artifacts[index] = utils.Artifact.read_artifact(
                    artifacts[index])
            utils.check_type(artifacts[index], utils.Artifact, errors.StateArtifactError, False,
                             f"Every artifact must be of type utils.Artifact: found {type(artifacts[index])}")
            if artifacts[index].getAction() != action:
                raise errors.StateArtifactError(
                    f"Found artifact for action {artifacts[index].getAction()} in {action} result")
            if artifacts[index].getEnv() != env:
                raise errors.StateArtifactError(
                    f"Found artifact for env {artifacts[index].getEnv()} in {action} result of env {env}")

    def set_result(self, result: dict, action: str, env=None):
        """
        This method is used to set the result of executing an action on the resource

        args:
            result (dict): The result object that we want to store in state.
            action (str): The action that generated this result.
            env (str|None): The env that the action was executed in, if None store the result in no_env

        raises:
            errors.StateError: When result, action or env types are wrong
        """
        utils.check_action_env_result(action, env, result)
        self.__check_result_artifacts(result, action, env)
        if env is None:
            self.__no_env[action] = result.copy()
        else:
            if self.__envs.get(env) is None:
                self.__envs[env] = {
                    action: result.copy()
                }
            else:
                self.__envs[env][action] = result.copy()
        self.__updated_at = datetime.now()

    def get_result(self, action: str, env=None) -> utils.ImDict:
        """
        Retrieve a result immutable dictionary from the state.

        args:
            action (str): The action that we want to retrieve its result.
            env (str|None): The env where the action was executed.
        returns:
            utils.ImDict: An immutable dictionary of the result as it is stored in state.
        """
        utils.check_action_env(action, env)
        if env is None:
            return utils.ImDict(self.__no_env.get(action, {}))
        return utils.ImDict(self.__envs.get(env, {}).get(action, {}))

    def __get_result_key(self, action: str, key: str, env=None, default=None):
        """
        Get a key from the result of one or more actions
        """
        ret = {}
        if action == "":
            for ac in all_actions:
                if env is None:
                    ret[ac] = self.__no_env.get(ac, {}).get(key, default)
                else:
                    ret[ac] = self.__envs.get(env, {}).get(
                        ac, {}).get(key, default)
        else:
            if env is None:
                ret[action] = self.__no_env.get(action, {}).get(key, default)
            else:
                ret[action] = self.__envs.get(env, {}).get(
                    action, {}).get(key, default)
        if type(ret) == dict:
            return utils.ImDict(ret)
        elif type(ret) == list:  # TODO: Is this needed?
            return tuple(ret)
        return ret

    def get_artifacts(self, action: str, env=None) -> utils.ImDict:
        """
        Retrieve the artifacts in this state.

        args:
            action (str): The action which we want to retrieve artifacts for it
            env (str|None): The env where the action was executed.

        returns:
            utils.ImDict or tuple : An immutable dictionary or tuple of the artifacts object
        """
        utils.check_action_env(action, env)
        return self.__get_result_key(action, artifacts_key, env, [])

    def get_globals(self, action: str, env=None) -> utils.ImDict:
        """
        Retrieve the global values in this state.

        args:
            action (str): The action which we want to retrieve globals for it
            env (str|None): The env where the action was executed.

        returns:
            utils.ImDict: An immutable dictionary of the globals object
        """
        utils.check_action_env(action, env)
        return self.__get_result_key(action, globals_key, env, {})

    def get_hash(self) -> str:
        """
        Return the hash of this state.

        returns:
            str: The hash value
        """
        return self.__hash

    def get_resource_id(self) -> str:
        """
        Return the resource id of this state

        returns:
            str: The id of the resource.
        """
        return self.__resource_id

    def get_envs(self) -> utils.ImDict:
        """
        Return the immutable version of envs dictionary

        returns:
            utils.ImDict: An immutable dictionary which contains all envs and their execution results
        """
        return utils.ImDict(self.__envs)

    def get_no_env(self) -> utils.ImDict:
        """
        Return the immutable version of no_env dictionary

        returns:
            utils.ImDict:  An immutable dictionary which contains the no_env execution results
        """
        return utils.ImDict(self.__no_env)

    def get_env_names(self, action: str) -> list:
        """
        Returns a list of env names which the action was executed on them, if the action is "" then return only all envs

        args:
            action (str): The name of the action

        returns:
            list (str): A list of strings which contain the env names
        """
        if action == "":
            return [key for key, _ in self.__envs.items()]
        else:
            return [key for key, item in self.__envs.items() if item.get(action) != None]

    def add_dep(self, dep_id: str, dep_hash: str):
        """
        Add a new dependency with its hash

        args:
            dep_id (str): The id of the dependency to add
            dep_hash (str): The hash of the dependecny to add
        """
        utils.check_type(dep_id, str, errors.StateError, False,
                         f"dep_id should be string: found {type(dep_id)}")
        utils.check_type(dep_hash, str, errors.StateError, False,
                         f"dep_hash should be string: found {type(dep_hash)}")
        self.__deps[dep_id] = dep_hash

    def get_deps(self) -> utils.ImDict:
        """
        Return an immutable dictionary of all dependencies with their hashes

        returns:
            utils.ImDict: An immutable dictionary of all dependencies with their hashes
        """
        return utils.ImDict(self.__deps)

    def get_dep(self, dep_id: str) -> str:
        """
        Return the hash of a single dependency

        args:
            dep_id (str): The id of the dependency to return its hash

        returns:
            str: The hash of the dependency, None if the id does not exist
        """
        utils.check_type(dep_id, str, errors.StateError, False,
                         f"dep_id should be string: found {type(dep_id)}")
        return self.__deps.get(dep_id)

    def set_status(self, last_action: str, error: str):
        """
        Set the status of the state, it contains the last action that was ran without errors
        and the last action that caused an error if possible.

        args:
            last_action (str): The last action without an error
            error (str): The last action with an error
        """
        utils.check_type(last_action, str, errors.StateError, False,
                         f"last action should be sring: found {type(last_action)}")
        utils.check_type(error, str, errors.StateError, False,
                         f"error should be sring: found {type(error)}")
        if last_action != "" and last_action not in all_actions:
            raise errors.StateError(
                f"last_action must be a valid action found {last_action}")
        if error != "" and error not in all_actions:
            raise errors.StateError(
                f"error must be a valid action found {error}")
        self.__status = {
            "last_action": last_action,
            "error": error
        }

    def get_status(self) -> utils.ImDict:
        """
        Return the status immutable dictionary of the state

        returns:
            utils.ImDict: An immutable dictionary of the status
        """
        return utils.ImDict(self.__status)

    def get_json_str(self, return_id=False) -> str:
        """
        Return a string JSON representation of the state

        args:
            return_id (bool): A boolean value that controls if we should return resource ID in state or not

        returns:
            str: The string JSON representation
        """
        ret = {
            "hash": self.get_hash(),
            "deps": self.get_deps(),
            "envs": self.get_envs(),
            "no_env": self.get_no_env(),
            "status": self.get_status(),
            "__updated_at": self.__updated_at
        }
        if return_id:
            ret["resource_id"] = self.get_resource_id()
        return json.dumps(ret, cls=utils.HashJsonEncoder)

    def get_json(self, return_id=False) -> str:
        """
        Return a JSON representation of the state

        args:
            return_id (bool): A boolean value that controls if we should return resource ID in state or not

        returns:
            dict: The JSON representation
        """
        ret = {
            "hash": self.get_hash(),
            "deps": self.get_deps(),
            "envs": self.get_envs(),
            "no_env": self.get_no_env(),
            "status": self.get_status(),
            "__updated_at": self.__updated_at
        }
        if return_id:
            ret["resource_id"] = self.get_resource_id()
        return ret

    def last_error(self) -> str:
        """
        Return the last action that caused an error, return "" if no error exists

        returns:
            str: The last action that caused an error
        """
        return self.__status.get("error", "")

    def last_action(self) -> str:
        """
        Return the last action exeucted without an error, if no action was executed return ""

        returns:
            str: The last action without an error
        """
        return self.__status.get("last_action", "")

    def copy_state(self, st):
        """
        A method to copy everything from another state object except for hash and resource ID

        args:
            st (State): The other state object to copy
        """
        self.__envs = st.get_envs().copy()
        self.__no_env = st.get_no_env().copy()
        self.__deps = st.get_deps().copy()
        self.__status = st.get_status().copy()
        self.__updated_at = self.get_updated_at().copy()

    def get_imdict(self) -> utils.ImDict:
        """
        Return a read only dictionary of the state.

        returns:
            utils.ImDict: An immutable dictionary of the entire state
        """
        return utils.ImDict({
            "hash": self.__hash,
            "resource_id": self.__resource_id,
            "envs": self.__envs,
            "no_env": self.__no_env,
            "deps": self.__deps,
            "status": self.__status
        })

    @classmethod
    def read_state(cls, state: dict, resource_id=None):
        """
        A classmethod to convert a state dictionary into a valid state object.

        args:
            state (dict): The dictionary that we want to convert into a state
            resource_id (str): The ID of resource, it is used only if the ID is not stored in state.

        returns:
            State: A State object
        """
        utils.check_type(state, dict, errors.StateError, False,
                         f"State must be a dictionary: found {type(state)}")
        _resource_id = state.get("resource_id")
        if _resource_id is None:
            utils.check_type(resource_id, str, errors.StateError, False,
                             f"Passed resource id must be string: found {type(resource_id)}")
        else:
            utils.check_type(_resource_id, str, errors.StateError, False,
                             f"State resource id must be string: found {type(resource_id)}")
            resource_id = _resource_id
        st = cls(state.get("hash"), resource_id)
        status = state.get("status", {})
        utils.check_type(status, dict, errors.StateError, False,
                         f"Status must be dictionary: found {type(status)}")
        st.set_status(status.get("last_action", ""), status.get("error", ""))
        deps = state.get("deps", {})
        utils.check_type(deps, dict, errors.StateError, True,
                         f"deps must be a list: found {type(deps)}")
        for dep_id, dep_hash in deps.items():
            st.add_dep(dep_id, dep_hash)
        envs = state.get("envs", {})
        utils.check_type(envs, dict, errors.StateError, False,
                         f"envs must be a dictionary: found {type(envs)}")
        for env_name, v in envs.items():
            utils.check_type(env_name, str, errors.StateError, False,
                             f"env name must be string: found {type(env_name)}")
            utils.check_type(v, dict, errors.StateError, False,
                             f"env actions must be a dictionary: found {type(v)}")
            for ac_name, result in v.items():
                st.set_result(result, ac_name, env_name)
        no_env = state.get("no_env", {})
        utils.check_type(no_env, dict, errors.StateError, False,
                         f"no_env must be a dictionary: found {type(envs)}")
        for ac_name, result in no_env.items():
            st.set_result(result, ac_name)
        return st
