"""
This module is used to create an execution plan to run action x on resource y in enviornment z and returns it as a graph
"""

from hash import utils, core, errors, resources
from hash.dag import Node
from hash.resources.base import EnvResource, Resource, ResourceSpace
from hash.core.templates import Renderer
from hash.dag import Edge, Graph
from .action import Action, is_action_less


def getKey(resource, action, env, _hash) -> str:
    if resource.getKind() == "Env":
        return f"{action}:{resource.getId()}:{resource.getName()}:{_hash}"
    if env is not None:
        return f"{action}:{resource.getId()}:{env.getName()}:{_hash}"
    return f"{action}:{resource.getId()}:None:{_hash}"


class Planner(object):
    """
    This class is used to create an execution plan for running action x on resource y in environment z
    """

    def __init__(self, store, base_path="") -> None:
        self.__store = store
        self.__base_path = base_path
        self.__space = ResourceSpace(self.__base_path)
        self.__graph = Graph()
        self.__n1 = None
        self.__states = {}
        self.__deps = {}
        self.env_deps = []

    def get_states(self):
        return self.__states

    def get__deps(self):
        return self.__deps

    @staticmethod
    def re_action(action: str, resource, state: utils.ImDict, _hash: str, deps=utils.ImDict({}), environment=None, base_path="") -> bool:
        """
        This method is used to check if we need to re-run the action on the resource given input state.

        args:
            action (str): The action that we want tocheck if we must re-run it
            resource (resources.Resource): The resource on which the action will be executed
            state (utils.ImDict): The current state for the resource
            _hash (str): The current hash of the resource
            deps (dict): A dictionary of deps IDs and their hashes, these will be compared with current deps in state to check if deps changed
                or not.
            environment (resources.EnvResource): The env to check against, use the object's env if passed as none.
            base_path (str): A base path used to create absolute paths for scripts

        returns:
            bool: True if we need to re-run the action on the resource given the state and env
        """
        utils.check_type(state, utils.ImDict, errors.ActionError, False,
                         f"State must be immutable dictionary : found {type(state)}")
        utils.check_type(_hash, str, errors.ActionError, False,
                         f"Hash must be string : found {type(_hash)}")
        utils.check_type(environment, resources.EnvResource, errors.ActionError,
                         True, f"Env must be EnvResource : found {type(environment)}")
        utils.check_type(deps, utils.ImDict, errors.ActionError, True,
                         f"Deps must be an immutable dictionary: found {type(deps)}")
        utils.check_action(action)
        if not action in core.all_actions:
            raise errors.ActionError(
                f"Unsupported action : found {action}, expected: {core.all_actions}")
        if state["hash"] != _hash:
            return True
        if state.get("status", {}).get("error") == action:
            return True
        if deps != utils.ImDict({}):
            state_deps = state.get("deps", {})
            if state_deps == utils.ImDict({}):
                return True
            else:
                for k, v in deps.items():
                    if state_deps.get(k) == None:
                        return True
                    else:
                        if state_deps.get(k) != v:
                            return True
        actions = []
        if environment is None:
            env = state.get("no_env")
            if env:
                actions = env.keys()
        else:
            env = state.get("envs", {}).get(environment.getName())
            if env:
                actions = env.keys()
        if action not in actions:
            return True
        action_obj = Action(action, resource, state, environment, base_path)
        if action_obj.re_action():
            return True
        return False

    def get_deps_with_hash(self, resource, deps):
        ret_deps = []
        for dep in deps:
            dep_id = dep.get("id")
            dep_res = self.__space.find_resource_by_id(dep_id)
            if dep_res is None:
                raise errors.ResourceConfigError(
                    f"No resource with ID {dep_id}, found in depends_on of resource {resource.getId()}")
            dep_hash = self.__space.calculate_hash(dep_res)
            ret_deps.append({
                "id": dep_id,
                "hash": dep_hash,
                "action1": dep.get("action1"),
                "action2": dep.get("action2")
            })
        return ret_deps

    def get_deps_metadata(self, resource: Resource):
        """
        Retrieve a dictionary of deps and their hashes from the resource's metadata
        """
        deps = resource.get_deps()
        return self.get_deps_with_hash(resource, deps)

    def get_deps_specs(self, resource: Resource, spec=None):
        """
        Retrieve a dictionary of deps and their hashes from the resource's specs attributes
        """
        deps = resource.get_deps_spec()
        return self.get_deps_with_hash(resource, deps)

    def get_deps_templates(self, resource: Resource):
        """
        Retrieve a dictionary of deps from the resource's templates
        TODO: to be implemented later
        """
        r = Renderer(resource, self.__space, None, None)
        return self.get_deps_with_hash(resource, r.get_deps())

    def get_deps(self, resource, env=None):
        """
        This method checks for all deps for the resource and return them as a list of dictionaries,
        Every dictionary has id key which is the resource's IDs, action1, action2 and hash keys.
        First it reads metadata.depends_on for all explicit deps, then it check the deps
        from the resource's attributes and then it checks deps from hash templates
        """
        deps_from_metadata = self.get_deps_metadata(resource)
        final_deps = deps_from_metadata
        deps_from_spec = self.get_deps_specs(resource)
        for dep in deps_from_spec:
            add = True
            for d in final_deps:
                if d["id"] == dep["id"] and d["action1"] == dep["action1"] and d["action2"] == dep["action2"]:
                    add = False
                    break
            if add:
                final_deps.append(dep)
        deps_from_templates = self.get_deps_templates(resource)
        for dep in deps_from_templates:
            add = True
            for d in final_deps:
                if d["id"] == dep["id"] and d["action1"] == dep["action1"] and d["action2"] == dep["action2"]:
                    add = False
                    break
            if add:
                final_deps.append(dep)
        deps_env = []
        if resource.getKind() != "Env":
            env_name = resource.getMetadata("env")
            if env_name is None:
                if env is not None:
                    deps_env = self.get_deps_with_hash(
                        resource, [{"id": env.getId(), "action2": "deploy"}])
            else:
                env = self.__space.find_resource_by_id(f"Env:{env_name}")
                if env is None:
                    raise errors.ResourceSpecError(
                        f"No env called {env_name} found in env metadata for resource {resource}")
                deps_env.extend(self.get_deps_with_hash(
                    resource, [{"id": env.getId(), "action2": "deploy"}]))
        final_deps.extend(deps_env)
        return final_deps

    def addEdge(self, node1: Node, node2: Node = None):
        if node2 is None:
            self.__n1 = node1
        else:
            if self.__n1:
                self.__graph.addEdge(Edge(node2, self.__n1))
                self.__graph.addEdge(Edge(node1, node2))
                self__n1 = None
            else:
                self.__graph.addEdge(Edge(node1, node2))

    def planAction(self, action: str, resource: Resource, env: EnvResource, state: utils.ImDict, deps):
        # TODO test inputs
        if resource.getKind() == "Env":
            env = resource
        env_name = resource.getMetadata("env")
        if resource.getKind() != "Env" and env_name is not None:
            env = self.__space.find_resource_by_id(f"Env:{env_name}")
            if env is None:
                raise errors.ResourceSpecError(
                    f"No env called {env_name} found in env metadata for resource {resource}")
        dd = {}
        for d in deps:
            dd[d["id"]] = d["hash"]
        print(f"Plan action {action} on {resource} in {env}")
        _hash = state["hash"]  # TODO: this cannot be true?!!!
        nodes = []
        least_action = None
        for ac in core.all_actions:
            if self.re_action(ac, resource, state, _hash, utils.ImDict(dd), env, self.__base_path):
                nodes.append(Node(getKey(resource, ac, env, _hash), {}))
                if least_action is None:
                    least_action = ac
            if ac == action:
                break
        if len(nodes) == 1:
            self.__graph.addNode(nodes[0])
            return least_action
        for i in range(0, len(nodes), 1):
            if i + 1 < len(nodes):
                self.addEdge(nodes[i], nodes[i+1])
        return least_action

    def getGraph(self):
        return self.__graph

    def plan(self, action: str, resource: Resource, env: EnvResource, state: utils.ImDict, process_env=True):
        if process_env == True:
            deps = self.get_deps(resource, env)
        else:
            deps = self.get_deps(resource, None)
        if resource.getKind() == "Env":
            self.env_deps.extend([x.get("id") for x in deps])
        if process_env is False:
            self.env_deps.append(resource.getId())
        self.__deps[resource.getId()] = deps
        resource.setSpace(self.__space)
        dep_ress = []
        for dep in deps:
            dep_id = dep.get("id")
            dep_res = self.__space.find_resource_by_id(dep_id)
            if dep_res is None:
                raise errors.ResourceConfigError(
                    f"No dependecny with id {dep_id}, it was found in deps of {resource.getId()}")
            dep_state = self.__store.get(dep_id, dep["hash"])
            self.__states[dep_id] = dep_state
            if dep["action1"] is not None and not is_action_less(dep["action1"], action):
                continue
            action2 = dep.get("action2")
            if action2 is None:
                action2 = action
            if resource.getKind() == "Env":
                least_action = self.plan(
                    action2, dep_res, env, dep_state.get_imdict(), False)
            else:
                least_action = self.plan(
                    action2, dep_res, env, dep_state.get_imdict(), process_env)
            if least_action is not None:
                dep_ress.append(
                    {"res": dep_res, "action": action2, "hash": dep["hash"]})
        least_action = self.planAction(action, resource, env, state, deps)
        env_name = resource.getMetadata("env")
        env_original = env
        if resource.getKind() != "Env" and env_name is not None:
            env = self.__space.find_resource_by_id(f"Env:{env_name}")
            if env is None:
                raise errors.ResourceSpecError(
                    f"No env called {env_name} found in env metadata for resource {resource}")
        for dep_res in dep_ress:
            res = dep_res["res"]
            res_env_name = res.getMetadata("env")
            if res.getKind() != "Env" and res_env_name is not None:
                env_res = self.__space.find_resource_by_id(
                    f"Env:{res_env_name}")
                if env_res is None:
                    raise errors.ResourceSpecError(
                        f"No env called {res_env_name} found in env metadata for resource {env_res}")
            else:
                env_res = env_original
            if least_action is None:
                self.__graph.addNode(
                    Node(getKey(dep_res["res"], dep_res["action"], env_res, dep_res["hash"]), {}))
            else:
                if dep_res["res"].getKind() == "Env" and resource.getMetadata("env") != dep_res["res"].getName():
                    if resource.getId() not in self.env_deps:
                        self.addEdge(Node(getKey(dep_res["res"], dep_res["action"], env_res, dep_res["hash"]), {
                        }), Node(getKey(resource, least_action, env, state["hash"]), {}))
                else:
                    self.addEdge(Node(getKey(dep_res["res"], dep_res["action"], env_res, dep_res["hash"]), {
                    }), Node(getKey(resource, least_action, env, state["hash"]), {}))
        return least_action
