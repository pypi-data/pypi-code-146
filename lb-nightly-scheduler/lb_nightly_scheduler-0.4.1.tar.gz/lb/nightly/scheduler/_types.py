###############################################################################
# (c) Copyright 2020-2022 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging
import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from time import sleep
from typing import Any, Iterable, Optional, Union

import luigi
import requests
from lb.nightly.configuration import DataProject, Package, Project, Slot
from lb.nightly.configuration import get as _get
from lb.nightly.configuration import lbnightly_settings, service_config
from lb.nightly.utils.Repository import connect

TIME_BETWEEN_DEPLOYMENT_CHECKS = timedelta(minutes=1)
MAX_TIME_WAITING_FOR_DEPLOYMENT = timedelta(hours=1)
TIME_BETWEEN_ARTIFACT_CHECKS = TIME_BETWEEN_DEPLOYMENT_CHECKS

logger = logging.getLogger("luigi-interface")


def _search(dct, path: Iterable[str]):
    """
    Simple helper to extract a value from nested (JSON-like)
    dictionaries.

    >>> _search({"foo":{"bar":{"baz":42}}}, ["foo", "bar", "baz"])
    42
    >>> _search({"good": 1}, ["bad"])
    >>>
    """
    try:
        for p in path:
            dct = dct[p]
        return dct
    except (KeyError, TypeError):
        # The specified path is not reachable
        return None


class ArtifactTarget(luigi.target.Target):
    def __init__(
        self,
        project: Union[Project, Package, Slot],
        stage: str,
        platform: str = "",
    ):
        from lb.nightly.db.database import Database

        conf = service_config()
        artifacts_repo = conf.get("artifacts", {}).get("uri") or os.environ.get(
            "LBNIGHTLY_ARTIFACTS_REPO"
        )
        self.repo = connect(artifacts_repo)
        self.docname = Database.docname(
            project if isinstance(project, Slot) else project.slot
        )
        try:
            self.path_in_doc = [
                {"checkout": "checkout", "build": "builds", "test": "tests"}[stage],
                platform or "projects",
                project.name,
                "artifact",
            ]
        except KeyError:
            raise ValueError("invalid stage {!r}".format(stage))

    @property
    def artifact_name(self):
        import lb.nightly.db

        return _search(lb.nightly.db.connect()[self.docname], self.path_in_doc)

    def exists(self, wait_for_it: Optional[timedelta] = None):
        # cache the artifact name
        artifact_name = self.artifact_name
        # check right away if it's there
        if artifact_name and self.repo.exist(artifact_name):
            return True
        if wait_for_it:
            # start loop to check at regular intervals
            start = datetime.now()
            while datetime.now() - start < MAX_TIME_WAITING_FOR_DEPLOYMENT:
                sleep(TIME_BETWEEN_ARTIFACT_CHECKS.total_seconds())
                # this keeps on checking if the artifact name can be obtained
                # from the doc and use the cached result once found
                artifact_name = artifact_name or self.artifact_name
                if artifact_name and self.repo.exist(artifact_name):
                    return True
        # not found (right away or waiting)
        return False


class DeploymentTarget(luigi.target.Target):
    def __init__(
        self,
        project: Union[Project, Package, Slot],
        stage: str,
        platform: str = "",
    ):
        conf = service_config()
        artifacts_repo = conf.get("artifacts", {}).get("uri") or os.environ.get(
            "LBNIGHTLY_ARTIFACTS_REPO"
        )
        self.repo = connect(artifacts_repo)
        self.artifact_name = project.artifacts(stage, platform)
        self.stage = stage
        self.deployment_dir = project.get_deployment_directory()
        self.project = project.name
        self.platform = platform
        self.item = project

    def deployment_ready(self):
        if self.stage == "checkout":
            return self.deployment_dir.exists() and any(
                item
                for item in self.deployment_dir.iterdir()
                if item.name not in {"InstallArea", ".cvmfscatalog"}
            )
        elif self.stage == "build":
            build_path = self.deployment_dir / "InstallArea" / self.platform
            return build_path.exists() and any(build_path.iterdir())
        elif self.stage == "deployment_dir":
            return (self.deployment_dir / "slot-config.json").exists()
        elif self.stage == "test":
            return True
        return False

    def trigger_deployment(
        self,
        artifact_name: Optional[str] = None,
    ) -> Any:
        """
        Makes a request to lbtask infrastructure to trigger installation
        of the deployment directory, sources or binaries.
        Returns json reponse content with the task id.
        """
        try:
            conf = service_config()
            hook = conf["lbtask"]["hook"]
            token = conf["lbtask"]["token"]
        except KeyError as exc:
            raise RuntimeError(
                f"cannot trigger cache installation due to missing settings: {exc}"
            )
        try:
            # Just check if we can have a URL to the artifact usable by the cvmfs installation process
            self.repo.get_url("an_artifact")
        except (NotImplementedError, AttributeError):
            raise RuntimeError(
                "Cannot trigger installation of artifacts from the repository other than Http and S3"
            )
        if isinstance(self.item, Slot):
            # installing slot deployment directory
            req = requests.put(
                f"{hook}/{self.item.id()}/",
                params={
                    "url": self.repo.get_url(self.item.artifacts("deployment_dir"))
                },
                headers={"Authorization": f"Bearer {token}"},
            )
        elif isinstance(self.item, DataProject):
            raise ValueError(
                f"Cannot trigger cache installation for {self.item} which is a DataProject"
            )
        elif isinstance(self.item, Project):
            if self.platform:
                # which implies installing binaries
                # the item here is of type Project
                # otherwise `artifacts()` will raise ValueError
                if not artifact_name:
                    raise ValueError(
                        "The artifact name has to be specified for "
                        "triggering binary installation"
                    )
                req = requests.put(
                    f"{hook}/{self.item.id()}/InstallArea/{self.platform}/",
                    params={"url": self.repo.get_url(artifact_name)},
                    headers={"Authorization": f"Bearer {token}"},
                )
            else:
                # installing sources for Project
                req = requests.put(
                    f"{hook}/{self.item.id()}/",
                    params={"url": self.repo.get_url(self.item.artifacts("checkout"))},
                    headers={"Authorization": f"Bearer {token}"},
                )
        elif isinstance(self.item, Package):
            # installing sources for Package
            req = requests.put(
                f"{hook}/{self.item.id()}/",
                params={"url": self.repo.get_url(self.item.artifacts("checkout"))},
                headers={"Authorization": f"Bearer {token}"},
            )
        else:
            raise ValueError(
                f"Cannot trigger cache installation for {self.item} (of type: {type(self.item)}), which is neither Project, neither Package nor Slot"
            )
        req.raise_for_status()
        return req.json()

    def wait_for_deployment(self):
        start = datetime.now()
        while datetime.now() - start < MAX_TIME_WAITING_FOR_DEPLOYMENT:
            if self.deployment_ready():
                return
            sleep(TIME_BETWEEN_DEPLOYMENT_CHECKS.total_seconds())
        # FIXME: instead of giving up, perhaps re-trigger deployment?
        logger.error(
            f"Giving up after waiting for deployment "
            f"of {self.item} {self.platform} {self.stage} artifact "
            f"for {MAX_TIME_WAITING_FOR_DEPLOYMENT}"
        )

    def exists(self):
        return self.deployment_ready()


class SlotParameter(luigi.parameter.Parameter):
    def parse(self, slot: str):
        """
        Expect a string like "[flavour/]slotname[/build_id]" and return the slot
        instance.
        """
        return _get(slot)

    def serialize(self, slot: Slot):
        """"""
        return slot.id()


class ProjectParameter(luigi.parameter.Parameter):
    def parse(self, project: str):
        """
        Expect a string like "[flavour/]slotname[/build_id]/project" and return the slot
        instance.
        """
        return _get(project)

    def serialize(self, project: Union[Project, Package]):
        """"""
        return project.id()


def do_report_exception(task, err: Exception):
    """
    Helper function to record an exception to a task summary in the database.
    """
    from lb.nightly.db import connect

    def get_section(doc, names):
        """
        Helper to get a dictionary from a collection of
        nested dictionaries.
        """
        for name in names:
            if name in doc:
                doc = doc[name]
            else:
                doc = doc[name] = {}
        return doc

    task_type = task.__class__.__name__
    if task_type == "Checkout":
        path = ["checkout", "projects", task.project.name]
    elif task_type in ("Build", "Test"):
        path = [f"{task_type.lower()}s", task.platform, task.project.name]
    else:
        # ignore unknown task types
        logger.warning(
            f"{task_type} is not supported in the context of recording an exception to a task summary in the database"
        )
        path = None

    if path:

        def update_doc(doc):
            info = get_section(doc, path)
            info["exception"] = {
                "time": str(datetime.now()),
                "desc": str(err),
            }

        db = connect()
        db.apply(update_doc, db[task.project.slot])


def report_exception(func):
    """
    Decorate a function so that if it raises an exception it is
    recorded in the matching document an re-raised.
    """
    from functools import wraps
    from inspect import isgeneratorfunction

    if isgeneratorfunction(func):

        @wraps(func)
        def wrapper(task):
            try:
                yield from func(task)
            except Exception as err:
                do_report_exception(task, err)
                raise

    else:

        @wraps(func)
        def wrapper(task):
            try:
                return func(task)
            except Exception as err:
                do_report_exception(task, err)
                raise

    return wrapper
