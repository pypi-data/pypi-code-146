"""
This module is used to render templates for a resource and clear them, it needs resource, state and globals as input
"""

import os
import shlex
import subprocess
import json
import jinja2
import uuid

from hash.utils import Artifacts, Template, Globals

from hash import errors


def raise_resource_error(name, e):
    if name == "build":
        raise errors.ResourceBuildError(e)
    elif name == "test":
        raise errors.ResourceTestError(e)
    elif name == "publish":
        raise errors.ResourcePublishError(e)
    elif name == "deploy":
        raise errors.ResourceDeployError(e)
    else:
        raise errors.ResourceError(e)


class Renderer(object):
    def __init__(self, resource, space, states, globs, env=None) -> None:
        self.__resource = resource
        self.__space = space
        self.__states = states
        self.__globs = globs
        self.__env = env

    def __get_hash_templates(self, path, recursive) -> list:
        if recursive is True:
            find_command = f"find {path} -type f -name *.hash"
        else:
            find_command = f"find {path} -maxdepth 1 -type f -name *.hash"
        find_command = shlex.split(find_command)
        path = os.path.join(self.__space.get_base(), self.__resource.getPath())
        find = subprocess.run(find_command, cwd=path, stdout=subprocess.PIPE)
        return find.stdout.decode().split("\n")[:-1]

    def get_hash_templates(self):
        direct_templates = self.__get_hash_templates(".", False)
        templates = self.__resource.getSpec("templates", {})
        templates_files = []
        templates_dirs = []
        templates_dirs_loop = []
        if templates is not {}:
            templates_files = templates.get("file", [])
            template_dirs = templates.get("dirs", [])
            for dir in template_dirs:
                templates_dirs.extend(self.__get_hash_templates(dir, False))
            template_dirs_loop = templates.get("dirs_loop", [])
            for dir in template_dirs_loop:
                templates_dirs_loop.extend(
                    self.__get_hash_templates(dir, True))

        return templates_dirs + templates_dirs_loop + templates_files + direct_templates

    def get_artifact_by_id(self, id: str, action: str, name: str) -> dict:
        resource = self.__space.find_resource_by_id(id)
        if resource is None:
            raise errors.ResourceError(
                f"No resource with id {id}, and artifact {name}")
        if self.__env is None:
            artifacts = self.__states[id].get_artifacts(action, self.__env)
        elif type(self.__env) == str:  # TODO: This should not happen, investigate later
            artifacts = self.__states[id].get_artifacts(action, self.__env)
        else:
            artifacts = self.__states[id].get_artifacts(
                action, self.__env.getName())
        for artifact in artifacts[action]:
            if artifact.getId() == name:
                return artifact

    def get_envs(self, env_name=None, dry=False) -> dict:
        envs = {}
        resource = self.__resource
        parent = resource.getMetadata("parent")
        parents = [resource]
        while parent:
            resource = self.__space.find_resource_by_id(parent)
            if resource:
                parents.append(resource)
                parent = resource.getMetadata("parent")
            else:
                break
        parents.reverse()
        for parent in parents:
            env = parent.getSpec("envs", {})
            envs.update(env)
        globals = Globals(self.__globs, env_name, dry)
        envs["globals"] = globals
        artifacts = Artifacts(dry, self.get_artifact_by_id)
        envs["artifacts"] = artifacts
        return envs

    def get_deps(self):
        """
        Return deps defined in templates
        """
        hash_files = self.get_hash_templates()
        path = os.path.join(self.__space.get_base(), self.__resource.getPath())
        tmp = Template(path, True)
        envs = self.get_envs(None, True)
        for file in hash_files:
            try:
                tmp.template(file, **envs)
            except jinja2.exceptions.UndefinedError as e:
                pass
            except errors.TemplateRenderError:
                pass
        return envs["globals"].deps + envs["artifacts"].deps

    def render(self, env=None, dry=False, action=None):
        hash_files = self.get_hash_templates()
        path = os.path.join(self.__space.get_base(), self.__resource.getPath())
        tmp = Template(path, dry)
        envs = self.get_envs(env, dry)
        for file in hash_files:
            try:
                ret = tmp.template(file, **envs)
            except jinja2.exceptions.UndefinedError as e:
                if not dry:
                    raise_resource_error(
                        action, f"error during rendering file {file}: {e}")
            if dry:
                return envs
            else:
                new_file = ".".join(file.split(".")[:-1])
                new_file = os.path.join(path, new_file)
                with open(new_file, "w") as f:
                    f.write(ret)

    def clear(self) -> None:
        hash_files = self.get_hash_templates()
        path = os.path.join(self.__space.get_base(), self.__resource.getPath())
        for file in hash_files:
            new_file = ".".join(file.split(".")[:-1])
            new_file = os.path.join(path, new_file)
            try:
                os.remove(new_file)
            except FileNotFoundError:
                pass
