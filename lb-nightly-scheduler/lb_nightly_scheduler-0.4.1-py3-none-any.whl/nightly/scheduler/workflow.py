###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging
from datetime import timedelta
from tempfile import TemporaryFile

import luigi
from lb.nightly.configuration import DataProject, Slot, lbnightly_settings
from lb.nightly.db import connect
from lb.nightly.utils import make_slot_deployment_dir

from ._types import (
    ArtifactTarget,
    DeploymentTarget,
    ProjectParameter,
    SlotParameter,
    report_exception,
)

logger = logging.getLogger("luigi-interface")


class AbortedSlotError(Exception):
    def __str__(self):
        return "slot build {} aborted by {} at {}".format(*self.args)


def raise_if_aborted_slot(slot: Slot):
    import requests

    try:
        abort_info = requests.get(
            f"{lbnightly_settings().couchdb.url}/_design/state/_view/aborted",
            params={"key": f'"{slot.id()}"'},
        ).json()["rows"][0]["value"]
    except Exception:
        # keep going if something goes wrong retrieving the data
        return
    raise AbortedSlotError(slot.id(), abort_info.get("user"), abort_info.get("time"))


class Checkout(luigi.Task):
    project = ProjectParameter()

    def output(self):
        return ArtifactTarget(self.project, stage="checkout")

    @report_exception
    def run(self):
        raise_if_aborted_slot(self.project.slot)
        from lb.nightly.rpc import checkout

        checkout(self.project.id())

        if not self.output().exists(wait_for_it=timedelta(hours=1)):
            raise RuntimeError(f"problem with {self.project.id()} checkout")


class DeploySources(luigi.Task):
    project = ProjectParameter()

    def output(self):
        return DeploymentTarget(self.project, stage="checkout")

    def requires(self):
        return Checkout(project=self.project)

    def run(self):
        raise_if_aborted_slot(self.project.slot)
        install_id = self.output().trigger_deployment()
        logger.info(
            f"Triggered deployment of sources for {self.project.id()}. "
            f"See the status on: https://lhcb-core-tasks.web.cern.ch/tasks/result/{install_id}"
        )
        self.output().wait_for_deployment()


class DeployDataProject(luigi.WrapperTask):
    project = ProjectParameter()

    def requires(self):
        for package in self.project.packages:
            yield DeploySources(project=package)


class Build(luigi.Task):
    project = ProjectParameter()
    platform = luigi.Parameter()

    def output(self):
        return ArtifactTarget(self.project, stage="build", platform=self.platform)

    def requires(self):
        return Checkout(project=self.project)

    @report_exception
    def run(self):
        raise_if_aborted_slot(self.project.slot)

        # at this point we should be able to get the dependencies from
        # CouchDB
        from ._types import _get

        slot = _get(self.project.slot.id())
        for dep in slot.projects[self.project.name].dependencies():
            if dep in slot.projects and self.project.slot.projects[dep].enabled:
                if isinstance(self.project.slot.projects[dep], DataProject):
                    yield DeployDataProject(project=self.project.slot.projects[dep])
                else:
                    yield DeployBinaries(
                        project=self.project.slot.projects[dep],
                        platform=self.platform,
                    )

        from lb.nightly.rpc import build

        build(
            self.project.id(),
            self.platform,
        )

        if not self.output().exists(wait_for_it=timedelta(hours=1)):
            raise RuntimeError(f"problem with {self.project.id()} build")


class DeployBinaries(luigi.Task):
    project = ProjectParameter()
    platform = luigi.Parameter()

    def output(self):
        return DeploymentTarget(self.project, stage="build", platform=self.platform)

    def requires(self):
        return Build(project=self.project, platform=self.platform)

    def run(self):
        raise_if_aborted_slot(self.project.slot)
        install_id = self.output().trigger_deployment(
            self.input().artifact_name,
        )
        logger.info(
            f"Triggered deployment of {self.input().artifact_name} of binaries "
            f"for {self.project.id()} and {self.platform}. See the status on: "
            f"https://lhcb-core-tasks.web.cern.ch/tasks/result/{install_id}"
        )
        self.output().wait_for_deployment()


class Test(luigi.Task):
    project = ProjectParameter()
    platform = luigi.Parameter()

    def output(self):
        return ArtifactTarget(self.project, stage="test", platform=self.platform)

    def requires(self):
        return (
            Checkout(project=self.project),
            Build(project=self.project, platform=self.platform),
        )

    @report_exception
    def run(self):
        raise_if_aborted_slot(self.project.slot)
        from lb.nightly.rpc import test

        test(
            self.project.id(),
            self.platform,
        )

        if not self.output().exists(wait_for_it=timedelta(hours=1)):
            raise RuntimeError(f"problem with {self.project.id()} test")


class DeploymentDir(luigi.Task):
    slot = SlotParameter()

    def output(self):
        return DeploymentTarget(self.slot, stage="deployment_dir")

    def run(self):
        raise_if_aborted_slot(self.slot)
        out = self.output()

        if not out.repo.exist(out.artifact_name):
            with TemporaryFile() as tmpfile:
                make_slot_deployment_dir(self.slot, tmpfile)
                assert out.repo.push(
                    tmpfile, out.artifact_name
                ), "failed to upload artifacts"

            install_id = self.output().trigger_deployment()
            logger.info(
                f"Triggered deployment of deployment directory for {self.slot.id()}. "
                f"See the status on: https://lhcb-core-tasks.web.cern.ch/tasks/result/{install_id}"
            )

        out.wait_for_deployment()


class Slot(luigi.WrapperTask):
    slot = SlotParameter()

    def requires(self):
        def update_scheduler_task_id(doc):
            doc["scheduler_task_id"] = self.task_id

        db = connect()
        db.apply(update_scheduler_task_id, db[self.slot])

        yield DeploymentDir(slot=self.slot)

        for project in self.slot.activeProjects:
            if isinstance(project, DataProject):
                yield DeployDataProject(project=project)
            else:
                yield DeploySources(project=project)
                for platform in self.slot.platforms:
                    if not project.platform_independent:
                        yield DeployBinaries(project=project, platform=platform)
                        if not (self.slot.no_test or project.no_test):
                            yield Test(project=project, platform=platform)
