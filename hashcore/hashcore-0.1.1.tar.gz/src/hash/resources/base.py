
import shlex
import os
import subprocess
import json

import pluggy
from hash import resource_hookimpl as hookimpl

from hash import errors, utils, hash

from .targets import Target, get_target
all_actions = ["build", "test", "publish", "deploy"]

hookspec = pluggy.HookspecMarker("hash-resource")


class ResourceSpec:
    @hookspec
    def init(self, file):
        pass

    @hookspec
    def action(self, name, state, env):
        pass

    @hookspec
    def re_action(self, action, state, env):
        pass


class Resource(object):
    def __init__(self, file) -> None:
        self.__path = file
        data = utils.parse_resource_file(file)
        self.__kind = data["kind"]
        self.__metadata = data["metadata"]
        self.__name = self.__metadata["name"]
        self.__spec = data.get("spec", {})
        self.__space = None

    def __str__(self) -> str:
        return f"{self.getKind()}:{self.getName()}"

    def setSpace(self, space):
        self.__space = space

    def getSpace(self):
        return self.__space

    def getPath(self):
        return os.path.join(os.path.dirname(self.__path), self.getSpec("path", "."))

    def getFile(self):
        return self.__path

    def getKind(self):
        return self.__kind

    def getName(self):
        return self.__name

    def getSpec(self, key, default=None):
        return self.__spec.get(key, default)

    def getMetadata(self, key, default=None):
        return self.__metadata.get(key, default)

    def getId(self):
        return f"{self.__kind}:{self.__name}"

    def forbidden_fields(self):  # skipcq: PYL-R0201
        """
            A list of forbidden fields that are not allowed
            to be mutated by Envs or Projects
        """
        return ["path"]

    def raise_resource_error(self, name, e):
        if name == "build":
            raise errors.ResourceBuildError(e)
        elif name == "test":
            raise errors.ResourceTestError(e)
        elif name == "publish":
            raise errors.ResourcePublishError(e)
        elif name == "deploy":
            raise errors.ResourceDeployError(e)

    def create_artifact(self, id: str, action: str, env: str, hash: str, kind: str, data: str):
        relative_path = ""
        if kind == "file":
            if data.startswith(self.getPath()):
                relative_path = data[len(self.getPath()) + 1:]
            else:
                relative_path = data.split("/")[-1]
        return utils.Artifact(id, action, env, hash, kind, data, relative_path)

    def getSpecDict(self):
        """
        Return a dictionary that contains a key for every attribute with an imutable version of its value
        """
        ret = {}
        for k, v in self.__spec.items():
            if type(v) == list:
                item = tuple(v)
            elif type(v) == dict:
                item = utils.ImDict(v)
            else:
                item = v
            ret[k] = item
        return ret

    @classmethod
    def execute(cls, command: str, path: str, timeout=300) -> subprocess.CompletedProcess:
        return subprocess.run(command, cwd=path, check=True, capture_output=True, shell=True, timeout=timeout)

    def createArtifact(self, id, kind, data):
        relative_path = ""
        if kind == "file":
            if data.startswith(self.getPath()):
                relative_path = data[len(self.getPath()) + 1:]
            else:
                relative_path = data.split("/")[-1]
        return utils.Artifact(id, "", "", "", kind, data, relative_path)

    def getParentId(self):
        parent_id = self.__metadata.get("parent")
        if parent_id is None:
            return
        utils.check_type(parent_id, str, errors.ResourceError, True,
                         f"parent ID must be string: found {type(parent_id)}")
        parent_parts = parent_id.split(":")
        if len(parent_parts) != 2 or parent_parts[1] == "" or parent_parts[0] == "":
            raise errors.ResourceError(f"Invalid parent ID: {parent_id}")
        return parent_id

    def mutate(self, mutate_spec: dict):
        """
        Mutate the specs of the resource based on mutation spec

        args:
            mutate_spec (dict): The specs used to mutate the resource
        """
        foribidden_fields = self.forbidden_fields() + ["path"]
        for field in foribidden_fields:
            if mutate_spec.get(field) != None:
                del mutate_spec[field]
        for k, v in self.__spec.items():
            if type(v) == list and mutate_spec.get(k) is not None:
                mutate_spec[k] = v + mutate_spec.get(k)
            elif type(v) == dict and mutate_spec.get(k) is not None:
                mutate_spec[k].update(v)
        self.__spec.update(mutate_spec)

    def __get_global(self, _globals, res_id, action, key, env):
        if env is None:
            env_name = "no_env"
        else:
            env_name = env
        if _globals.get(res_id) is None:
            raise errors.ResourceSpecError(
                f"No globals for resource with id {res_id}")
        if _globals[res_id].get(env_name) is None:
            raise errors.ResourceSpecError(
                f"No globals for resource with id {res_id} in env {env_name}")
        if _globals[res_id][env_name].get(action) is None:
            raise errors.ResourceSpecError(
                f"No globals for resource with id {res_id} in env {env_name} for action {action}")
        if _globals[res_id][env_name][action].get(key) is None:
            raise errors.ResourceSpecError(
                f"No globals for resource with id {res_id} in env {env_name}, action {action} called {key}")
        return _globals[res_id][env_name][action][key]

    def __fill_specs(self, env: str, _globals: dict, rs, spec: dict):
        keys = {}
        delete_keys = {}
        for i, v in spec.items():
            if type(v) == str and v.startswith("$"):
                parts = v.split(".")
                if len(parts) > 2:
                    res_id = parts[0][1:]
                    action = parts[1]
                    res = rs.find_resource_by_id(res_id)
                    if res is None:
                        raise errors.ResourceSpecError(
                            f"No resource with id : {res_id}")
                    if res.getMetadata("env"):
                        result = self.__get_global(
                            _globals, res_id, action, parts[2], res.getMetadata("env"))
                    else:
                        result = self.__get_global(
                            _globals, res_id, action, parts[2], env)
                    for p in parts[3:]:
                        try:
                            result = result[p]
                        except KeyError:
                            raise errors.ResourceSpecError(
                                f"Resource with id {res_id}, does not have an output called {p} from action {action} and env {env}")
                    spec[i] = result
            elif type(i) == str and i.startswith("$"):
                parts = i.split(".")
                if len(parts) > 2:
                    res_id = parts[0][1:]
                    action = parts[1]
                    res = rs.find_resource_by_id(res_id)
                    if res is None:
                        raise errors.ResourceSpecError(
                            f"No resource with id {res_id}")
                    if res.getMetadata("env"):
                        result = self.__get_global(
                            _globals, res_id, action, parts[2], res.getMetadata("env"))
                        delete_keys[i] = 1
                    else:
                        result = self.__get_global(
                            _globals, res_id, action, parts[2], env)
                        delete_keys[i] = 1
                    for p in parts[3:]:
                        try:
                            result = result[p]
                        except KeyError:
                            raise errors.ResourceSpecError(
                                f"Resource with id {res_id}, does not have an output called {p} from action {action} and env {env}")
                    keys[result] = v
                    delete_keys[i] = 1
            elif type(v) == dict:
                self.__fill_specs(env, _globals, rs, v)
            elif type(v) == list:
                for item in v:
                    if type(item) == dict:
                        self.__fill_specs(env, _globals, rs, item)
        if keys != {}:
            for i, v in keys.items():
                spec[i] = v
        if delete_keys != {}:
            for i, v in delete_keys.items():
                del spec[i]

    def fill_specs(self, env: str, _globals: dict, rs):
        """
        Fill the resources specs with data according to the env and globals, every spec
        key/value that starts with $ is filled according to current env and globals

        args:
            env (str): The env from which we must fill the specs
            _globals (dict): A dictionary for global values to use when sub-situting
                keys/values that start with $
            rs (ResourceSpace): The space in which to search for resources
        """
        self.__fill_specs(env, _globals, rs, self.__spec)

    def get_deps(self):
        """
        Return a list of explicit deps for this resource
        """
        deps = self.getMetadata("depends_on", [])
        utils.check_type(deps, list, errors.ResourceConfigError,
                         False, f"depends_on should be a list: found {type(deps)}")
        ret_deps = []
        ids = []
        for dep in deps:
            utils.check_type(dep, dict, errors.ResourceConfigError,
                             False, f"Every dep should be a dictionary: found")
            dep_id = dep.get("id")
            if dep_id in ids:
                continue
            ids.append(dep_id)
            utils.check_type(dep_id, str, errors.ResourceConfigError, False,
                             f"Every dep needs to have an ID of type string: found {type(dep_id)}")
            ret_deps.append(dep)
        return ret_deps

    def process_value(self, v, deps):
        if type(v) == str and v.startswith("$"):
            parts = v.split(".")
            if len(parts) > 2:
                res_id = parts[0][1:]
                action = parts[1]
                deps.append({"id": res_id, "action2": action})
        elif type(v) == dict:
            deps.extend(self.get_deps_spec(v))
        elif type(v) == list:
            for item in v:
                if type(item) == str and item.startswith("$"):
                    parts = item.split(".")
                    if len(parts) > 2:
                        res_id = parts[0][1:]
                        action = parts[1]
                        deps.append({"id": res_id, "action2": action})
                elif type(item) == dict:
                    deps.extend(self.get_deps_spec(item))

    def get_deps_spec(self, spec=None):
        if spec is None:
            spec = self.__spec
        deps = []
        for k, v in spec.items():
            self.process_value(k, deps)
            self.process_value(v, deps)
        return deps


class FakeResource(Resource):
    @hookimpl
    def init(self, file):
        pass

    @hookimpl
    def action(self, name, state, env):
        if name not in all_actions:
            raise errors.ResourceError(
                f"Fake resource only supports these actions {all_actions}")
        ret = {
            f"{name}_result": self.getSpec(f"{name}_result"),
            "globals": self.getSpec("globals")
        }
        # process artifacts
        artifacts = self.getSpec("artifacts", [])
        afts = []
        env_name = None
        if env is not None:
            env_name = env.getName()
        for aft in artifacts:
            if aft.get("kind") == "file":
                content = aft.get("content")
                if content is not None:
                    with open(os.path.join(self.getPath(), aft.get("path")), "w") as f:
                        f.write(content)
                af = self.create_artifact(aft.get("id", "id"), name, env_name, state.get(
                    "hash"), "file", os.path.join(self.getPath(), aft.get("path")))
                afts.append(af)
            else:
                af = self.create_artifact(aft.get("id", "id"), name, env_name, state.get(
                    "hash"), aft.get("kind"), aft.get("data"))
                afts.append(af)
        ret["artifacts"] = afts
        if self.getSpec("ret"):
            return self.getSpec("ret")
        return ret

    def forbidden_fields(self):
        return ["dont"]

    @hookimpl
    def re_action(self, action, state, env):
        return self.getSpec(f"re_{action}", False)


class EnvResource(Resource):
    def action(self, name, state, env):
        pass

    def getTarget(self, kind: str):
        targets = self.getSpec("targets", [])
        for target in targets:
            if target["kind"] == kind:
                return get_target(kind, target, self.getSpace())
        parent_id = self.getParentId()
        if parent_id:
            parent = self.getSpace().find_resource_by_id(parent_id)
            if parent is None:
                raise errors.ResourceSpecError(
                    f"No resource with id {parent_id} in metadata of {self.getId()}")
            targets = parent.getSpec("targets", [])
            for target in targets:
                if target["kind"] == kind:
                    return get_target(kind, target, self.getSpace())

    def __str__(self) -> str:
        return self.getName()


class ProjectResource(Resource):
    def action(self, name, state, env):
        pass

    def __str__(self) -> str:
        return self.getName()


class TerraformResource(Resource):
    def select_workspace(self, workspace):
        workspace_new_command = f"terraform workspace new {workspace}"
        try:
            self.execute(workspace_new_command, self.getPath())
        except Exception:
            pass
        workspace_select_command = f"terraform workspace select {workspace}"
        self.execute(workspace_select_command, self.getPath())

    def terraform_init(self, workspace):
        init_command = "terraform init -upgrade -input=false -force-copy"
        state_backend = self.getSpec("state_backend")
        if state_backend:
            kind = state_backend.get("kind", "gcs")
            if kind == "gcs":
                bucket_name = state_backend.get("bucket_name")
                if bucket_name is None:
                    raise errors.ResourceConfigError(
                        "GCS backend requires bucket_name option")
                prefix = state_backend.get("prefix")
                if prefix:
                    init_command += f" -backend-config='bucket={bucket_name}' -backend-config='prefix={prefix}'"
                else:
                    init_command += f" -backend-config='bucket={bucket_name}'"
                project = state_backend.get("project")
                if project:
                    p = self.execute(f"gsutil ls -p {project}", self.getPath())
                else:
                    p = self.execute(f"gsutil ls", self.getPath())
                if bucket_name not in p.stdout.decode("UTF-8"):
                    location = state_backend.get("location", "EU")
                    if project:
                        gcs_command = f"gsutil mb -l {location} -p {project} gs://{bucket_name}"
                    else:
                        gcs_command = f"gsutil mb -l {location} gs://{bucket_name}"
                    self.execute(gcs_command, self.getPath())
            else:
                raise errors.ResourceConfigError(
                    f"Unknown state backend kind: {kind}")

        self.execute(init_command, self.getPath())
        self.select_workspace(workspace)

    @hookimpl
    def init(self, file: str):
        """
            Initialize the terraform resource.

            Args:
                content (dict): The dictionary that represents the YAML file resource, it must
                have a key called kind with the value of Terraform, a key called metadata with
                a dictionary value which at least has a name key, a key called spec with a
                dictionary value which at least hash a path key that must exist.
        """
        super().__init__(file)
        if self.getKind() != "Terraform":
            raise errors.ResourceConfigError(
                "This is not a terraform resource")
        self.name = self.getMetadata("name")

    def get_outputs(self, path) -> dict:
        try:
            refresh_command = "terraform refresh"
            variables = self.getSpec("variables")
            if variables:
                vars = ""
                for (var_name, var_value) in variables.items():
                    if type(var_value) == list:
                        value = str(var_value).replace("\'", "\"")
                        vars += f" -var '{var_name}={value}'"
                    else:
                        vars += f" -var {var_name}={var_value}"
                refresh_command += vars
            self.execute(refresh_command, path)
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)
        try:
            proc = self.execute("terraform output -json", path)
            return json.loads(proc.stdout)
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)

    @hookimpl
    def action(self, name, state, env):
        if name == "build":
            return self.build(state, env)
        elif name == "test":
            return self.test(state, env)
        elif name == "deploy":
            return self.deploy(state, env)

    def build(self, state: dict, env: EnvResource):
        """
        Build the terraform resource based on its resource file

        Args:
            base_path (str): This path is joined with the path in the spec
            to get the full path to the terraform files directory.
        """
        if env is None or env == {}:
            self.raise_resource_error(
                "build", "Terraform resource requires an env with workspace argument")
        workspace = env.getSpec("workspace", env.getName())
        try:
            self.terraform_init(workspace)
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(
                f"Cannot initialize terraform, {e}")
        except subprocess.TimeoutExpired as e:
            raise errors.ResourceBuildError(
                f"Timeout initializing terraform, {e}")
        build_command = "terraform plan -out=tfplan -no-color -input=false"
        variables = self.getSpec("variables")
        if variables:
            vars = ""
            for (var_name, var_value) in variables.items():
                if type(var_value) == list:
                    value = str(var_value).replace("\'", "\"")
                    vars += f" -var '{var_name}={value}'"
                else:
                    vars += f" -var {var_name}={var_value}"
            build_command += vars
        try:
            self.execute(build_command, self.getPath(),
                         self.getSpec("plan_timeout", 300))
        except FileNotFoundError as e:
            raise errors.ResourceBuildError("cannot find terraform in PATH")
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e.stderr.decode("UTF-8"))
        artifacts = [self.create_artifact("tfplan", "build", env.getName(), state.get(
            "hash", ""), "file", os.path.join(self.getPath(), "tfplan"))]
        return {"status": "plan generated", "artifacts": artifacts, "globals": self.get_outputs(self.getPath())}

    def test(self, state: dict, env: EnvResource):
        fmt_check_command = "terraform fmt --check"
        try:
            self.execute(fmt_check_command, self.getPath())
        except subprocess.CalledProcessError as e:
            raise errors.ResourceTestError(
                f"Terraform is not formatted probably: please run command `terraform fmt`, {e}")
        except subprocess.TimeoutExpired as e:
            raise errors.ResourceTestError(
                f"Timeout checking terraform format, {e}")
        return {
            "error": False,
            "message": "terraform is fomratted probably"
        }

    def deploy(self, state: dict, env: EnvResource):
        """
        Build the terraform resource based on its resource file

        Args:
            base_path (str): This path is joined with the path in the spec
            to get the full path to the terraform files directory.
        """
        if env is None or env == {}:
            self.raise_resource_error(
                "deploy", "Terraform resource requires an env with workspace argument")
        workspace = env.getSpec("workspace", env.getName())
        try:
            self.terraform_init(workspace)
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(
                f"Cannot initialize terraform, {e}")
        except subprocess.TimeoutExpired as e:
            raise errors.ResourceBuildError(
                f"Timeout initializing terraform, {e}")
        deploy_command = "terraform apply -input=false -auto-approve -no-color"
        variables = self.getSpec("variables")
        if variables:
            vars = ""
            for (var_name, var_value) in variables.items():
                if type(var_value) == list:
                    value = str(var_value).replace("\'", "\"")
                    vars += f" -var '{var_name}={value}'"
                else:
                    vars += f" -var {var_name}={var_value}"
            deploy_command += vars
        try:
            self.execute(deploy_command, self.getPath(),
                         self.getSpec("apply_timeout", 300))
            return {"status": "plan applied", "globals": self.get_outputs(self.getPath())}
        except FileNotFoundError as e:
            raise errors.ResourceBuildError("cannot find terraform in PATH")
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e.stderr.decode("UTF-8"))

# Kustomize resource


class KustomizeResource(Resource):
    @hookimpl
    def init(self, file: str):
        """
            Initialize the kustomize resource.

            Args:
                content (dict): The dictionary that represents the YAML file resource, it must
                have a key called kind with the value of Kustomize, a key called metadata with
                a dictionary value which at least has a name key, a key called spec with a
                dictionary value which at least hash a path key that must exist.
        """
        super().__init__(file)
        if self.getKind() != "Kustomize":
            raise errors.ResourceConfigError(
                "This is not a kustomize resource")
        self.name = self.getMetadata("name")

    @classmethod
    def generate(cls, path, file):
        build_command = "kustomize build"
        try:
            p = cls.execute(build_command, path)
        except FileNotFoundError as e:
            raise errors.ResourceBuildError("Cannot find kustomize in PATH")
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e.stderr.decode("UTF-8"))
        path = os.path.join(path, file)
        with open(path, "w") as f:
            f.write(p.stdout.decode("UTF-8"))

    @hookimpl
    def action(self, name, state, env):
        if name == "build":
            return self.build(state, env)
        elif name == "test":
            return self.test(state, env)
        elif name == "deploy":
            return self.deploy(state, env)

    def build(self, state: dict, env: EnvResource):
        """
        Build the kustomize resource based on its resource file

        Args:
            base_path (str): This path is joined with the path in the spec
            to get the full path to the kustomize files directory.
        """
        path = os.path.join(
            self.getPath(), f"artifact-manifests-{self.name}.yaml")
        self.generate(self.getPath(), f"artifact-manifests-{self.name}.yaml")
        artifact = self.create_artifact(
            "manifests", "build", env.getName(), state.get("hash", ""), "file", path)
        return {"msg": "manifests generated", "artifacts": [artifact]}

    @classmethod
    def runTests(cls, target: Target, path: str, artifacts: list):
        test_command = "kustomize build -o=/dev/null"
        try:
            cls.execute(test_command, path)
        except FileNotFoundError as e:
            raise errors.ResourceTestError("Cannot find kustomize in PATH")
        except subprocess.CalledProcessError as e:
            raise errors.ResourceTestError(e.stderr.decode("UTF-8"))
        if target:
            for artifact in artifacts:
                config = {
                    "path": path,
                    "manifests_path": artifact.getData()
                }
                try:
                    target.action("test", config)
                except errors.ResourceError as e:
                    raise errors.ResourceTestError(str(e))

    @classmethod
    def applyManifests(cls, env: EnvResource, path: str, artifacts: list):
        if env is None:
            raise errors.ResourceDeployError(
                "You need an env to apply k8s manifests")
        target = env.getTarget("K8STarget")
        if target is None:
            raise errors.ResourceDeployError(
                f"No K8S target found in env {env.getName()}")
        for artifact in artifacts:
            config = {
                "path": path,
                "manifests_path": artifact.getData()
            }
            try:
                target.action("deploy", config)
            except errors.ResourceError as e:
                raise errors.ResourceDeployError(str(e))

    def test(self, state: dict, env: EnvResource):
        if env is None:
            artifacts = state["no_env"]["build"].get("artifacts", [])
        else:
            artifacts = state["envs"][env.getName()]["build"].get(
                "artifacts", [])
            target = env.getTarget("K8STarget")
            if target is None:
                raise errors.ResourceTestError(
                    f"No target of kind K8STarget in env {env}")
        self.runTests(target, self.getPath(), artifacts)
        return {"msg": "kustomize tested without errors"}

    def deploy(self, state: dict, env: EnvResource):
        if env is None:
            artifacts = state["no_env"]["build"].get("artifacts", [])
        else:
            artifacts = state["envs"][env.getName()]["build"].get(
                "artifacts", [])
        self.applyManifests(env, self.getPath(), artifacts)
        return {"msg": "kustomize applied without errors"}

# Docker resource


class DockerImageResource(Resource):
    @classmethod
    def build_image_name(cls, res, state):
        image_name = res.getSpec("image_name", res.name)
        image_tag = res.getSpec("image_tag")
        if image_tag:
            image_name += ":" + image_tag + "-" + state["hash"][:6]
        else:
            image_name += ":" + state["hash"][:6]
        return image_name

    @hookimpl
    def init(self, file: str):
        """
            Initialize the Docker Image resource.

            Args:
                content (dict): The dictionary that represents the YAML file resource.
        """
        super().__init__(file)
        if self.getKind() != "DockerImage":
            raise errors.ResourceConfigError(
                "This is not a DockerImage resource")
        self.name = self.getMetadata("name")

    @classmethod
    def DockerBuild(cls, path, image_name, docker_file="Dockerfile"):
        build_command = f"docker build -t {image_name} . -f {docker_file}"
        try:
            cls.execute(build_command, path)
            return {"error": False, "msg": "built docker image"}
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)

    @hookimpl
    def action(self, name, state, env):
        if name == "build":
            return self.build(state, env)
        elif name == "test":
            return self.test(state, env)
        elif name == "publish":
            return self.publish(state, env)
        elif name == "deploy":
            return self.deploy(state, env)

    def build(self, state: dict, env: EnvResource):
        image_name = self.build_image_name(self, state)
        ret = self.DockerBuild(self.getPath(), image_name,
                               self.getSpec("docker_file", "Dockerfile"))
        save_command = f"docker save {image_name} -o docker.build"
        try:
            self.execute(save_command, self.getPath())
            ret["artifacts"] = [
                self.create_artifact("image_file", "build", env.getName(
                ), state["hash"], "file", os.path.join(self.getPath(), "docker.build"))
            ]
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)
        return ret

    @classmethod
    def runTests(cls, image_name, path, accept_latest=False, docker_file="Dockerfile"):
        test_command = f"docker build -t {image_name} . -f {docker_file}"
        try:
            cls.execute(test_command, path)
        except subprocess.CalledProcessError as e:
            raise errors.ResourceTestError(e)
        if accept_latest:
            return
        with open(os.path.join(path, docker_file)) as f:
            line = f.readline()
            while line:
                parts = line.split(" ")
                if len(parts) > 1:
                    if parts[0] == "FROM":
                        second_part = parts[1].split(":")
                        if len(second_part) == 1:
                            raise errors.ResourceTestError(
                                Exception(f"no tag is specified for image {second_part[0]}"))
                        else:
                            if second_part[1].strip() == "latest":
                                raise errors.ResourceTestError(
                                    Exception(f"latest tag is specified for image {second_part[0]}"))
                line = f.readline()

    def test(self, state: dict, env: EnvResource):
        image_name = self.build_image_name(self, state)
        self.runTests(image_name, self.getPath(), self.getSpec(
            "accept_latest", False), self.getSpec("docker_file", "Dockerfile"))
        return {"error": False, "msg": "tested docker image"}

    def publish(self, state: dict, env: EnvResource):
        if env is None:
            raise errors.ResourcePublishError(
                "Cannot publish Docker resource without an env")
        artifacts = state["envs"][env.getName()]["build"].get("artifacts", [])
        image_name = self.build_image_name(self, state)
        config = {
            "path": self.getPath(),
            "image_name": image_name,
            "docker_file": self.getSpec("docker_file", "Dockerfile"),
            "image_file": os.path.join(self.getPath(), "docker.build")
        }
        target = env.getTarget("DockerRegistryTarget")
        if target is None:
            raise errors.ResourceDeployError(
                f"No Docker Registry target found in env {env.getName()}")
        image_url = target.action("publish", config)
        return {
            "artifacts": [self.create_artifact("image_url", "publish", env.getName(), state.get("hash", ""), "url", image_url)]
        }

    def deploy(self, state: dict, env: EnvResource):
        if env is None:
            raise errors.ResourceDeployError(
                "Cannot deploy Docker resource without an env")
        artifacts = state["envs"][env.getName()]["publish"].get(
            "artifacts", [])
        image_url = artifacts[0].getData()
        config = {
            "path": self.getPath(),
            "kind": "DockerImage",
            "port": self.getSpec("expose_port"),
            "service_account": self.getSpec("service_account"),
            "pod_name": self.getSpec("pod_name", self.name),
            "image_url": image_url
        }
        target = env.getTarget("K8STarget")
        if target is None:
            raise errors.ResourceDeployError(
                f"No K8S target found in env {env.getName()}")
        target.action("deploy", config)

# Go Service resource


class GoServiceResource(Resource):
    @hookimpl
    def init(self, file: str):
        """
            Initialize the GoService resource.

            Args:
                content (dict): The dictionary that represents the YAML file resource.
        """
        super().__init__(file)
        if self.getKind() != "GoService":
            raise errors.ResourceConfigError(
                "This is not a GoService resource")
        self.name = self.getMetadata("name")

    @classmethod
    def compile(cls, go_executable, executable_name, path):
        go_version_command = f"{go_executable} version"
        ret = {}
        try:
            r = cls.execute(go_version_command, path)
            r = r.stdout.decode("utf-8")
            ret["version"] = r.split(" ")[2][2:]
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)
        compile_command = f"{go_executable} build -o {executable_name} ."
        try:
            cls.execute(compile_command, path)
            return ret
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)

    @classmethod
    def runTests(cls, go_executable, golangci_lint_executable, path):
        golangci_lint_version_command = f"{golangci_lint_executable} version"
        ret = {}
        try:
            r = cls.execute(golangci_lint_version_command, path)
            r = r.stdout.decode("utf-8")
            ret["version"] = r.split(" ")[3]
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)
        lint_command = f"{golangci_lint_executable} run"
        test_command = f"{go_executable} test ./..."
        try:
            cls.execute(lint_command, path)
            cls.execute(test_command, path)
            return ret
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e.output.decode("utf-8"))

    @hookimpl
    def action(self, name, state, env):
        if name == "build":
            return self.build(state, env)
        elif name == "test":
            return self.test(state, env)

    def build(self, state: dict, env: EnvResource):
        executable_name = self.getSpec("exec_name", self.name)
        self.compile("go", executable_name, self.getPath())
        artifact = self.create_artifact("binary", "build", env.getName(
        ), state["hash"], "file", os.path.join(self.getPath(), executable_name))
        return {
            "status": "Go Service compiled without errors",
            "artifacts": [artifact]
        }

    def test(self, state: dict, env: EnvResource):
        self.runTests("go", "golangci-lint", self.getPath())
        return {
            "status": "Go service tested without errors"
        }

    @hookimpl
    def re_action(state: dict, action: str, env={}) -> bool:
        return False


class MicroService(object):
    @classmethod
    def build(cls, res, state, target):
        docker_path = os.path.join(
            res.getPath(), res.getSpec("docker_path", "."))
        image_name = DockerImageResource.build_image_name(res, state)
        config = {
            "image_name": image_name,
            "path": res.getPath()
        }
        image_url = target.action("publish", config)
        k8s_path = os.path.join(res.getPath(), res.getSpec("k8s_path", "k8s"))
        KustomizeResource.generate(k8s_path, "manifests.yaml")
        k8s_file = os.path.join(k8s_path, "manifests.yaml")
        try:
            with open(k8s_file, "r") as f:
                if f.read() == "" and not res.getSpec("allow_empty_manifests", True):
                    raise errors.ResourceBuildError(
                        "Empty manifests file and allow_empty_manifests is set to false")
        except FileNotFoundError:
            if not res.getSpec("allow_empty_manifests", True):
                raise errors.ResourceBuildError(
                    "Empty manifests file and allow_empty_manifests is set to false")
            else:
                with open(k8s_file, "w") as f:
                    f.write("")
        os.environ["IMAGE_URL"] = image_url
        try:
            command = f"cat manifests.yaml | envsubst"
            p = subprocess.run(command, cwd=k8s_path, check=True,
                               capture_output=True, shell=True, timeout=10)
            with open(k8s_file, "w") as f:
                f.write(p.stdout.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            raise errors.ActionError(
                f"Cannot replace IMAGE URL in manifests file : error {p.stderr.decode('utf-8')}")
        return image_url, k8s_file

    @classmethod
    def test(cls, res, target, artifacts):
        # Test docker image
        image_name = res.getSpec("image_name", res.name)
        DockerImageResource.runTests(image_name, res.getPath())

        # Test k8s manifests
        for artifact in artifacts:
            if artifact.getId() == "k8s":
                k8s_path = os.path.join(
                    res.getPath(), res.getSpec("k8s_path", "k8s"))
                KustomizeResource.runTests(target, k8s_path, [artifact])
                break

    @classmethod
    def deploy(cls, res, target, artifacts):
        config = {
            "path": res.getPath()
        }
        for artifact in artifacts:
            if artifact.getId() == "k8s":
                config["manifests_path"] = artifact.getData()
                target.action("deploy", config)
                break


# Go Micro Service resource
class GoMicroServiceResource(Resource):
    @hookimpl
    def init(self, file: str):
        """
            Initialize the GoMicroService resource.

            Args:
                content (dict): The dictionary that represents the YAML file resource.
        """
        super().__init__(file)
        if self.getKind() != "GoMicroService":
            raise errors.ResourceConfigError(
                "This is not a GoMicroService resource")
        self.name = self.getMetadata("name")
        self.__go_checksums = {
            "1.19.3": "74b9640724fd4e6bb0ed2a1bc44ae813a03f1e72a4c76253e2d5c015494430ba",
            "1.19.2": "5e8c5a74fe6470dd7e055a461acda8bb4050ead8c2df70f227e3ff7d8eb7eeb6",
            "1.19.1": "acc512fbab4f716a8f97a8b3fbaa9ddd39606a28be6c2515ef7c6c6311acffde",
            "1.19": "464b6b66591f6cf055bc5df90a9750bf5fbc9d038722bb84a9d56a2bea974be6",
            "1.18": "e85278e98f57cdb150fe8409e6e5df5343ecb13cebf03a5d5ff12bd55a80264f",
            "1.18.1": "b3b815f47ababac13810fc6021eb73d65478e0b2db4b09d348eefad9581a2334",
            "1.18.2": "e54bec97a1a5d230fc2f9ad0880fcbabb5888f30ed9666eca4a91c5a32e86cbc",
            "1.18.3": "956f8507b302ab0bb747613695cdae10af99bbd39a90cae522b7c0302cc27245",
            "1.18.4": "c9b099b68d93f5c5c8a8844a89f8db07eaa58270e3a1e01804f17f4cf8df02f5",
            "1.18.5": "9e5de37f9c49942c601b191ac5fba404b868bfc21d446d6960acc12283d6e5f2",
            "1.18.6": "bb05f179a773fed60c6a454a24141aaa7e71edfd0f2d465ad610a3b8f1dc7fe8",
            "1.18.7": "6c967efc22152ce3124fc35cdf50fc686870120c5fd2107234d05d450a6105d8",
            "1.18.8": "4d854c7bad52d53470cf32f1b287a5c0c441dc6b98306dea27358e099698142a",
        }
        self.__golangci_lint_checksums = {
            "1.50.1": "4ba1dc9dbdf05b7bdc6f0e04bdfe6f63aa70576f51817be1b2540bbce017b69a",
            "1.50.0": "b4b329efcd913082c87d0e9606711ecb57415b5e6ddf233fde9e76c69d9b4e8b",
            "1.49.0": "5badc6e9fee2003621efa07e385910d9a88c89b38f6c35aded153193c5125178"
        }
        self.__go = "go"
        self.__golangci_lint = "golangci-lint"

    def check_go(self):
        go_version = self.getSpec("go_version")
        if go_version:
            try:
                if os.path.isfile(os.path.join(self.getSpace().get_hash_dir(), f"go{go_version}.linux-amd64", "bin", "go")):
                    self.execute(f"{self.__go} version", self.getPath())
                    self.__go = os.path.join(self.getSpace().get_hash_dir(
                    ), f"go{go_version}.linux-amd64", "bin", "go")
            except subprocess.CalledProcessError as e:
                raise errors.ActionError(e)
        else:
            self.__go = "go"

    def check_golangci_lint(self):
        check_golangci_lint_version = self.getSpec("golangci_lint_version")
        if check_golangci_lint_version:
            try:
                if os.path.isfile(os.path.join(self.getSpace().get_hash_dir(), f"golangci-lint-{check_golangci_lint_version}-linux-amd64", "golangci-lint")):
                    self.execute(
                        f"{self.__golangci_lint} version", self.getPath())
                    self.__golangci_lint = os.path.join(self.getSpace().get_hash_dir(
                    ), f"golangci-lint-{check_golangci_lint_version}-linux-amd64", "golangci-lint")
            except subprocess.CalledProcessError as e:
                raise errors.ActionError(e)
        else:
            self.__golangci_lint = "golangci-lint"

    def __install_go(self, version: str):
        self.check_go()
        if self.__go != "go":
            return
        try:
            file_name = f"go{version}.linux-amd64.tar.gz"
            hash_dir = self.getSpace().get_hash_dir()
            self.execute(f"wget -c https://go.dev/dl/{file_name}", hash_dir)
            with open(os.path.join(hash_dir, "checksums.txt"), "w") as f:
                checksum = self.__go_checksums.get(
                    version, self.getSpec("go_checksum"))
                if checksum is None:
                    raise errors.ActionError(
                        f"version {version} doesn't have a checksum in specs or in the resource's class")
                f.write(f"{checksum} {file_name}")
            self.execute("sha256sum -c checksums.txt", hash_dir)
            self.execute(f"tar -zxf {file_name}", hash_dir)
            self.execute(f"mv go go{version}.linux-amd64", hash_dir)
            self.__go = os.path.join(
                hash_dir, f"go{version}.linux-amd64", "bin", "go")
        except subprocess.CalledProcessError as e:
            raise errors.ActionError(e)

    def __install_golangci_lint(self, version: str):
        self.check_golangci_lint()
        if self.__golangci_lint != "golangci-lint":
            return
        try:
            file_name = f"golangci-lint-{version}-linux-amd64.tar.gz"
            hash_dir = self.getSpace().get_hash_dir()
            self.execute(
                f"wget -c https://github.com/golangci/golangci-lint/releases/download/v{version}/{file_name}", hash_dir)
            with open(os.path.join(hash_dir, "checksums.txt"), "w") as f:
                checksum = self.__golangci_lint_checksums.get(
                    version, self.getSpec("golangci_lint_checksum"))
                if checksum is None:
                    raise errors.ActionError(
                        f"version {version} doesn't have a checksum in specs or in the resource's class")
                f.write(f"{checksum} {file_name}")
            self.execute("sha256sum -c checksums.txt", hash_dir)
            self.execute(f"tar -zxf {file_name}", hash_dir)
            self.__golangci_lint = os.path.join(
                hash_dir, f"golangci-lint-{version}-linux-amd64", "golangci-lint")
        except subprocess.CalledProcessError as e:
            raise errors.ActionError(e)

    def setup_tools(self):
        go_version = self.getSpec("go_version")
        if go_version:
            try:
                r = self.execute(f"{self.__go} version", self.getPath())
                r = r.stdout.decode("utf-8")
                version = r.split(" ")[2][2:]
                if version != go_version:
                    if not self.getSpec("go_install"):
                        raise errors.ActionError(
                            f"go version is {version}, required version {go_version} but go_install is not set to True")
                    self.__install_go(go_version)
            except subprocess.CalledProcessError as e:
                raise errors.ActionError(e)
        golangci_lint_version = self.getSpec("golangci_lint_version")
        if golangci_lint_version:
            try:
                r = self.execute(
                    f"{self.__golangci_lint} version", self.getPath())
                r = r.stdout.decode("utf-8")
                version = r.split(" ")[3]
                if version != golangci_lint_version:
                    if not self.getSpec("golangci_lint_install"):
                        raise errors.ActionError(
                            f"golangci-lint version is {version}, required version {golangci_lint_version} but golangci_lint_install is not set to True")
                    self.__install_golangci_lint(golangci_lint_version)
            except subprocess.CalledProcessError as e:
                raise errors.ActionError(e)

    @hookimpl
    def action(self, name, state, env):
        self.setup_tools()
        if name == "build":
            return self.build(state, env)
        elif name == "test":
            return self.test(state, env)
        elif name == "deploy":
            return self.deploy(state, env)

    def build(self, state: dict, env: EnvResource):
        if env is None:
            raise errors.ResourceBuildError(
                f"Building micro service {self} requires an env")
        target = env.getTarget("DockerRegistryTarget")
        if target is None:
            raise errors.ResourceBuildError(
                f"No target of kind DockerRegistry in env {env}")
        # Build go service
        executable_name = self.getSpec("exec_name", self.name)
        go_env_data = GoServiceResource.compile(
            self.__go, executable_name, self.getPath())
        executable_path = os.path.join(self.getPath(), executable_name)
        image_url, k8s_file = MicroService.build(self, state, target)

        binary_artifact = self.create_artifact(
            "binary", "build", env.getName(), state["hash"], "file", executable_path)
        k8s_artifact = self.create_artifact(
            "k8s", "build", env.getName(), state["hash"], "file", k8s_file)
        image_url_artifact = self.create_artifact(
            "image_url", "build", env.getName(), state["hash"], "url", image_url)
        return {
            "artifacts": [binary_artifact, k8s_artifact, image_url_artifact],
            "_go": go_env_data
        }

    def test(self, state: dict, env: EnvResource):
        if env is None:
            raise errors.ResourceTestError(
                f"Testing micro service {self} requires an env")
        target = env.getTarget("K8STarget")
        if target is None:
            raise errors.ResourceTestError(
                f"No target of kind K8STarget in env {env}")
        artifacts = state["envs"][env.getName()]["build"].get("artifacts", [])
        # Test go code
        golang_ci_lint_env_data = GoServiceResource.runTests(
            self.__go, self.__golangci_lint, self.getPath())

        MicroService.test(self, target, artifacts)
        return {
            "_golangci_lint": golang_ci_lint_env_data
        }

    def deploy(self, state: dict, env):
        # deploy k8s manifests only
        if env is None:
            raise errors.ResourceDeployError(
                f"Deploying micro service {self} requires an env")
        target = env.getTarget("K8STarget")
        if target is None:
            raise errors.ResourceDeployError(
                f"No target of kind K8STarget in env {env}")
        artifacts = state["envs"][env.getName()]["build"].get("artifacts", [])
        MicroService.deploy(self, target, artifacts)

    @hookimpl
    def re_action(self, action, state, env):
        if env is None:
            result = state.get("no_env")
        else:
            result = state.get("envs", {}).get(env.getName())
        self.check_go()
        go_version = result.get("build", {}).get("_go", {}).get("version")
        go_version_command = f"{self.__go} version"
        try:
            r = self.execute(go_version_command, self.getPath())
            r = r.stdout.decode("utf-8")
            version = r.split(" ")[2][2:]
            if version != go_version:
                return True
        except subprocess.CalledProcessError as e:
            raise errors.ResourceBuildError(e)
        return False


def get_plugin_manager():
    pm = pluggy.PluginManager("hash-resource")
    pm.add_hookspecs(ResourceSpec)
    pm.load_setuptools_entrypoints("hash-resource")
    pm.register(FakeResource, "FakeResource")
    pm.register(EnvResource, "EnvResource")
    pm.register(ProjectResource, "ProjectResource")
    pm.register(TerraformResource, "TerraformResource")
    pm.register(KustomizeResource, "KustomizeResource")
    pm.register(DockerImageResource, "DockerImageResource")
    pm.register(GoServiceResource, "GoServiceResource")
    pm.register(GoMicroServiceResource, "GoMicroServiceResource")
    return pm


def get_resource(file: str):
    """
    Retrun the specific resource object of the resource file
    passed as an argument

    args:
        file (str): The path to the resource's file
    """
    data = utils.parse_resource_file(file)
    kind = data["kind"] + "Resource"
    pm = get_plugin_manager()
    plugins = pm.list_name_plugin()
    for plugin in plugins:
        if kind == plugin[0]:
            hash_resource = plugin[1](file)
            if callable(getattr(hash_resource, "init", None)):
                hash_resource.init(file)
            return hash_resource


class ResourceSpace(object):
    def __init__(self, base: str) -> None:
        self.__base = base
        hash_dir = os.path.join(base, ".hash")
        if not os.path.isdir(hash_dir):
            os.mkdir(hash_dir)

    def read(self, file: str):
        path = os.path.join(self.__base, file)
        return get_resource(path)

    def find_resource_by_id(self, res_id):
        utils.check_type(res_id, str, errors.ResourceError, False,
                         f"resource id must be str: found {type(res_id)}")
        res_id_parts = res_id.split(":")
        if len(res_id_parts) != 2:
            raise errors.ResourceError(f"Invalid resource ID: {res_id}")
        return self.find_resource(res_id_parts[1], res_id_parts[0])

    def get_base(self):
        return str(self.__base)

    def get_hash_dir(self):
        return os.path.join(self.__base, ".hash")

    def find_resource(self, name: str, kind: str):
        """
        Search the workspace for a resource based on its namd and kind

        args:
            name (str): The name of the resource to find.
            kind (str): The kind of the resource to find
        """
        find_command = "find . -name *.yaml"
        find_command = shlex.split(find_command)
        find = subprocess.run(
            find_command, cwd=self.__base, stdout=subprocess.PIPE)
        resource_files = find.stdout.decode().split("\n")[:-1]
        for file in resource_files:
            f = file.split("/")[-1]
            if f.startswith("resource"):
                rs = self.read(file)
                if rs and rs.getKind() == kind and rs.getName() == name:
                    return rs

    def cal_spec(self, resource, env: str, _globals: dict):
        """
        This function updates the values of the resource's specs, based
        on the env and globals object

        args:
            resource (Resource): This is the resource which we want to update its spec
            env (str): The env in which the specs will be updated
            _globals (dict): A dictionary of the globals which are used to fill the
                values for specs which have $ in their names, values
        """
        env_id = f"Env:{env}"
        env_res = self.find_resource_by_id(env_id)
        if env_res is not None:
            mutate_spec_kind = env_res.getSpec(resource.getKind())
            if mutate_spec_kind:
                resource.mutate(mutate_spec_kind)
            resource_id = resource.getId().replace(":", "-")
            mutate_spec_id = env_res.getSpec(resource_id)
            if mutate_spec_id:
                resource.mutate(mutate_spec_id)
            parent_id = env_res.getParentId()
            if parent_id:
                parent_res = self.find_resource_by_id(parent_id)
                if parent_res is None:
                    raise errors.ResourceSpecError(
                        f"No resource with id {parent_id} in metatdata of {env_id}")
                mutate_spec_kind = parent_res.getSpec(resource.getKind())
                if mutate_spec_kind:
                    resource.mutate(mutate_spec_kind)
                resource_id = resource.getId().replace(":", "-")
                mutate_spec_id = parent_res.getSpec(resource_id)
                if mutate_spec_id:
                    resource.mutate(mutate_spec_id)

        resource.fill_specs(env, _globals, self)

    def calculate_hash(self, resource, alg="sha256"):
        if resource.getKind() == "Env":
            match = [resource.getFile().split("/")[-1]]
            match.extend(resource.getSpec("match", []))
            return hash.Hash(alg).hash(os.path.join(self.__base, resource.getPath()), match)
        match = resource.getSpec("match")
        if match:
            match.append(resource.getFile().split("/")[-1])
            match.append("*.hash")
        build_script = resource.getSpec("build_script")
        if build_script and match:
            match.append(build_script)
        if resource.getKind() == "Env":
            match = [resource.getFile().split("/")[-1]]
            match.extend(resource.getSpec("match", []))
        return hash.Hash(alg).hash(os.path.join(self.__base, resource.getPath()), match)
