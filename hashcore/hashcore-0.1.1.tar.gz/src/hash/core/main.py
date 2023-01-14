"""
The main core module, it has the main_action method which runs an action x on resource y in environment z
"""

from hash import errors
import os
from hash import core
from hash.core import Execute
from hash.core import Planner
from hash.resources import EnvResource, get_resource
from hash.resources.base import ResourceSpace


def main_action(resource_file: str, action_name: str, env_name: str, base_path: str, store):
    if os.path.isdir(resource_file):
        resource_file = os.path.join(resource_file, "resource.yaml")
    if not os.path.exists(resource_file):
        raise errors.ResourceError(f"File not found {resource_file}")
    resource = get_resource(resource_file)
    if resource is None:
        raise errors.ResourceError(
            f"Resource at {resource_file} is not recognized")
    rs = ResourceSpace(base_path)
    if env_name is None:
        env = None
    else:
        env = rs.find_resource_by_id(f"Env:{env_name}")
        if env is None:
            raise errors.ResourceError(f"No env with name {env_name}")
    h = rs.calculate_hash(resource)
    st = store.get(resource.getId(), h)
    pl = Planner(store, base_path)
    pl.plan(action_name, resource, env, st.get_imdict())
    deps = pl.get__deps()
    ex = Execute(rs, store, "SerialExecutor", pl.get_states())
    ex.execute(pl.getGraph())
    for _, state in ex.get_states().items():
        res_id = state.get_resource_id()
        _deps = deps.get(res_id, [])
        for dep in _deps:
            state.add_dep(dep.get("id"), dep.get("hash"))
        store.store(state)
    for ac in core.all_actions:
        artifacts = st.get_artifacts(ac, env_name).get(ac, [])
        for artifact in artifacts:
            if artifact.getKind() == "file":
                try:
                    os.remove(artifact.getData())
                except Exception:
                    pass
    for _, state in pl.get_states().items():
        for ac in core.all_actions:
            res = rs.find_resource_by_id(state.get_resource_id())
            if res:
                env_name_res = res.getMetadata("env")
                if env_name_res:
                    artifacts = state.get_artifacts(
                        ac, env_name_res).get(ac, [])
                else:
                    artifacts = state.get_artifacts(ac, env_name).get(ac, [])
            else:
                artifacts = state.get_artifacts(ac, env_name).get(ac, [])
            for artifact in artifacts:
                if artifact.getKind() == "file":
                    try:
                        os.remove(artifact.getData())
                    except Exception:
                        pass

    return ex.get_steps()
