""""
This module contains the Action class which represents executes a single action assuming all its deps are ready
"""

import os
import subprocess
from hash import errors, utils
from hash.resources import EnvResource, Resource
from .state import all_actions


def is_action_less(action1: str, action2: str) -> bool:
    if action1 == "build":
        return True
    if action1 == "test" and (action2 == "deploy" or action2 == "publish" or action2 == "test"):
        return True
    if action1 == "publish" and (action2 == "deploy" or action2 == "publish"):
        return True
    if action1 == "deploy" and action2 == "deploy":
        return True
    return False


class Action(object):
    """
    The Action class is used to execute a single action on a single resource with
    a state and en env, it assumes that all dependencies are ready and all templates
    are rendered for this resource.
    """

    def __init__(self, action: str, resource: Resource, state: utils.ImDict, env: EnvResource, base_path: str) -> None:
        """
        Action class initializer, it takes 5 arguments which are needed to execute the action

        args:
            action (str): The action string that we want to run it can be build, test, publish or deploy.
            resource (Resource): The resource object that we want to execute the action on it.
            state (utils.ImDict): The immutable version of the state for this resource.
            env (EnvResource): The environment object in which this action will be run.
            base_path (str): The base path for resources on disk, this is needed for executing action scripts if found.
        """
        utils.check_action(action)
        self.__action = action
        utils.check_type(state, utils.ImDict, errors.ActionError, False,
                         f"State must be an immutable dictionary: found {type(state)}")
        self.__state = state
        self.__resource = resource
        utils.check_type(env, EnvResource, errors.ActionError,
                         True, f"Env must be EnvResource: found {type(env)}")
        self.__env = env
        self.__base_path = base_path
        self.__path = os.path.join(self.__base_path, self.__resource.getPath())

    def raise_error(self, msg):
        if self.__action == "build":
            raise errors.ResourceBuildError(msg)
        elif self.__action == "test":
            raise errors.ResourceTestError(msg)
        elif self.__action == "publish":
            raise errors.ResourcePublishError(msg)
        elif self.__action == "deploy":
            raise errors.ResourceDeployError(msg)

    def get_json(self):
        if self.__env:
            return {
                "action": self.__action,
                "resource_id": self.__resource.getId(),
                "env": self.__env.getId()
            }
        return {
            "action": self.__action,
            "resource_id": self.__resource.getId(),
            "env": None
        }

    def setup_env(self) -> None:
        """
        This method is used to setup the environment for running a command or script on the resource, it
        sets these enviornment variables:

        R_NAME: It contains the name of the resource.
        R_PARENT: It contains the ID of parent resource (Kind:Name)
        R_PARENT_NAME: It contains the name of parent resource
        R_ENV: It contains the name of environment where the action is being executed.
        R_ACTION: It contains the current name of action being executed.
        R_SPEC_{X}: this defines a group of environment variables for every spec element, for example
        if you have a spec called 'x' with a value of 'abc' it will create an environment variable
        called R_SPEC_X with a value of 'abc'
        """
        os.environ["R_NAME"] = self.__resource.getName()
        parentId = self.__resource.getParentId()
        if parentId is None:
            parentId = ""
            parentName = ""
        else:
            parentName = parentId.split(":")[1]
        if self.__env is None:
            env = ""
        else:
            env = self.__env.getName()
        os.environ["R_ENV"] = env
        os.environ["R_ACTION"] = self.__action
        os.environ["R_PARENT"] = parentId
        os.environ["R_PARENT_NAME"] = parentName
        for k, v in self.__resource.getSpecDict().items():
            env_name = f"R_SPEC_{k.upper()}"
            os.environ[env_name] = str(v)

    def re_action(self):
        """
        Check if we need to re-run the action based on the resource's specs
        """
        re_action_command = self.__resource.getSpec(
            f"re_{self.__action}_command")
        if re_action_command:
            self.setup_env()
            try:
                self.__resource.execute(re_action_command, self.__path)
            except subprocess.CalledProcessError as e:
                if e.returncode == 1:
                    return True
                else:
                    pass  # TDOD: the return code chould be 1, what to do here?
        else:
            re_action_script = self.__resource.getSpec(
                f"re_{self.__action}_script")
            if re_action_script:
                self.setup_env()
                script = utils.Script(os.path.join(
                    self.__path, re_action_script))
                try:
                    script.run(self.__path)
                except subprocess.CalledProcessError as e:
                    if e.returncode == 1:
                        return True
                    else:
                        pass  # TDOD: the return code chould be 1, what to do here?
            else:
                if hasattr(self.__resource, "re_action") and callable(getattr(self.__resource, "re_action")):
                    if self.__resource.re_action(self.__action, self.__state, self.__env):
                        return True
        return False

    def do_pre_action(self):
        """
        Run pre action command or script on the resource, it searches for a spec
        called `pre_<action>_command` if found then it is executed, if not it searches
        for `pre_<action>_script` if found then it is executed and if not then the method
        returns.

        Before executing any command or script the values for environment variables are
        set using setup_env method
        """
        pre_action_command = self.__resource.getSpec(
            f"pre_{self.__action}_command")
        if pre_action_command:
            self.setup_env()
            self.__resource.execute(pre_action_command, self.__path)
        else:
            pre_action_script = self.__resource.getSpec(
                f"pre_{self.__action}_script")
            if pre_action_script:
                self.setup_env()
                script = utils.Script(os.path.join(
                    self.__path, pre_action_script))
                script.run(self.__path)

    def do_post_action(self):
        """
        Run post action command or script on the resource, it searches for a spec
        called `post_<action>_command` if found then it is executed, if not it searches
        for `post_<action>_script` if found then it is executed and if not then the method
        returns.

        Before executing any command or script the values for environment variables are
        set using setup_env method
        """
        post_action_command = self.__resource.getSpec(
            f"post_{self.__action}_command")
        if post_action_command:
            self.setup_env()
            self.__resource.execute(post_action_command, self.__path)
        else:
            post_action_script = self.__resource.getSpec(
                f"post_{self.__action}_script")
            if post_action_script:
                self.setup_env()
                script = utils.Script(os.path.join(
                    self.__path, post_action_script))
                script.run(self.__path)

    def do_action(self):
        """
        Run the actual action on the resource, it searches for `<action>_command`
        spec if found then it is ran, if not it searches for `<action>_script` spec
        if found then it is ran otherwise it calls `action` method on the resource and
        passes to it the action's name, state and env, the returned value is used
        as a return for this method, it no return value was found then it returns
        a default dictionary with one `msg` key, it also checks if the return value
        is not a dictionary, it raises an error according to the current action.
        """
        action_command = self.__resource.getSpec(f"{self.__action}_command")
        action_script = self.__resource.getSpec(f"{self.__action}_script")
        result = None
        if action_command:
            self.setup_env()
            self.__resource.execute(action_command, self.__path)
        elif action_script:
            if action_script:
                self.setup_env()
                script = utils.Script(os.path.join(self.__path, action_script))
                script.run(self.__path)
        else:
            result = self.__resource.action(
                self.__action, self.__state, self.__env)
            if result is not None and type(result) != dict:
                self.raise_error(
                    f"Returned value from action must be dict: found {type(result)}")
        if result is None:
            result = {
                "msg": f"Run {self.__action} without errors"
            }
        return result

    def run_action(self):
        """
        Run an action on a resource assuming all deps are ready and templates rendered

        It first calls pre action code, then calls the actual action and lastly the post action code.
        """
        if self.__action not in all_actions:
            raise errors.ActionError(
                f"Action {self.__action} not allowed: allowed actions are {all_actions}")
        print(
            f"Run action {self.__action} on resource {self.__resource} in env {self.__env}")
        self.do_pre_action()
        ret = self.do_action()
        self.do_post_action()
        return ret
