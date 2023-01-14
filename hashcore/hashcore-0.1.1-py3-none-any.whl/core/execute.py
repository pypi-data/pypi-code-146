"""
This module is used to execute the plan from the generated graph
"""

from hash import errors
from hash.core.templates import Renderer
from hash.dag import Graph
from .action import Action

import pluggy
from pytest import hookimpl

hookspec = pluggy.HookspecMarker("hash-executor")


class ExecutorSpec:
    @hookspec
    def run(self, ac):
        pass


class SerialExecutor:
    @hookimpl
    def run(self, act):
        return act.run_action()


class Execute(object):
    def __init__(self, space, store, kind, states) -> None:
        self.__space = space
        self.__store = store
        self.__kind = kind
        self.__states = states
        self.__steps = []
        self.__globals = self.__store.get_globals()

    def get_states(self):
        return self.__states

    def get_steps(self):
        return self.__steps

    def add_to_globals(self, result, ac, res, env):
        _globals = result.get("globals")
        if _globals is None:
            return
        if type(_globals) != dict:
            if env is None:
                raise errors.ResourceError(
                    f"Action {ac} on resource {res.getId()} returned globals of type {type(_globals)}, it must be dict")
            else:
                raise errors.ResourceError(
                    f"Action {ac} on resource {res.getId()} in env {env.getName()} returned globals of type {type(_globals)}, it must be dict")
        _res_globals = self.__globals.get(res.getId())
        if env is None:
            env_name = "no_env"
        else:
            env_name = env.getName()
        if _res_globals is None:
            self.__globals[res.getId()] = {
                env_name: {
                    ac: _globals
                }
            }
            return
        _env_globals = self.__globals[res.getId()].get(env_name)
        if _env_globals is None:
            self.__globals[res.getId()][env_name] = {
                ac: _globals
            }
            return
        _ac_globals = self.__globals[res.getId()][env_name].get(ac)
        if _ac_globals is None:
            self.__globals[res.getId()][env_name][ac] = _globals
            return
        self.__globals[res.getId()][env_name][ac] = _globals

    def execute(self, plan: Graph):
        steps = plan.walk_number()
        if steps is None:
            return
        index = 0
        step_list = steps[index]
        errors = []
        while step_list:
            for step in step_list:
                data = step.getKey().split(":")
                if len(data) < 4 or len(data) > 6:
                    raise errors.GraphError(f"Invalid data : {data}")
                res_id = f"{data[1]}:{data[2]}"
                action = data[0]
                env_id = f"Env:{data[3]}"
                if env_id == "Env:None":
                    env = None
                else:
                    env = self.__space.find_resource_by_id(env_id)
                res = self.__space.find_resource_by_id(res_id)
                error = self.execute_action(action, res, env, data[4])
                if error is not None:
                    errors.append(error)
            index += 1
            if len(errors) != 0:
                return errors
            if index >= len(steps):
                break
            step_list = steps[index]

    def execute_action(self, ac, res, env, _hash):
        state = self.__states.get(res.getId())
        if state is None:
            self.__states[res.getId()] = self.__store.get(res.getId(), _hash)
            state = self.__states.get(res.getId())
        r = Renderer(res, self.__space, self.__states, self.__globals, env)
        if env is None:
            self.__space.cal_spec(res, None, self.__globals)
            r.render(action=ac)
        else:
            self.__space.cal_spec(res, env.getName(), self.__globals)
            env.setSpace(self.__space)
            try:
                self.__space.cal_spec(env, env.getName(), self.__globals)
            except errors.ResourceSpecError:
                pass
            r.render(env=env.getName(), action=ac)
        res.setSpace(self.__space)
        act = Action(ac, res, state.get_imdict(), env, self.__space.get_base())
        executor = get_executor(self.__kind)
        if executor is None:
            raise errors.ExecutorErrorNotFound(
                f"No executor with kind {self.__kind}")
        else:
            try:
                step = act.get_json()
                step["error"] = False
                result = executor.run(act)
                status = state.get_status()
                if status.get("error") == ac:
                    state.set_status(ac, "")
            except errors.ResourceError as e:
                result = {
                    "error": True,
                    "msg": str(e)
                }
                state.set_status(ac, ac)
                step["error"] = True
                step["msg"] = str(e)
                return str(e)
            except Exception as e:
                result = {
                    "error": True,
                    "msg": f"Unkown error {str(e)}"
                }
                state.set_status(ac, ac)
                step["error"] = True
                step["msg"] = str(e)
                return str(e)
            finally:
                self.__steps.append(step)
                r.clear()
                artifacts = result.get("artifacts", [])
                base_path = self.__space.get_base()
                for art in artifacts:
                    if art.getKind() == "file":
                        relative_path = art.getData()[len(base_path) + 1:]
                        art.setRelativePath(relative_path)
                self.add_to_globals(result, ac, res, env)
                if env is None:
                    state.set_result(result, ac, None)
                else:
                    state.set_result(result, ac, env.getName())


def get_plugin_manager():
    pm = pluggy.PluginManager("hash-executor")
    pm.add_hookspecs(ExecutorSpec)
    pm.load_setuptools_entrypoints("hash-executor")
    pm.register(SerialExecutor, "SerialExecutor")
    return pm


def get_executor(kind: str):
    pm = get_plugin_manager()
    plugins = pm.list_name_plugin()
    for plugin in plugins:
        if kind == plugin[0]:
            return plugin[1]()
