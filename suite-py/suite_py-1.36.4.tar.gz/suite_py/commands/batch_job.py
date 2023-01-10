# -*- coding: utf-8 -*-
import re
import sys
import textwrap

import semver

from suite_py.lib import logger
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.drone_handler import DroneHandler
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.github_handler import GithubHandler


class BatchJob:
    def __init__(
        self, project, config, tokens, environment, cpu_request, memory_request
    ):
        self._project = project
        self._config = config
        self._tokens = tokens
        self._environment = environment
        self._cpu_request = cpu_request
        self._memory_request = memory_request
        self._git = GitHandler(project, config)
        self._github = GithubHandler(tokens)
        self._drone = DroneHandler(config, tokens, repo=project)
        self._countries = _parse_available_countries(self._drone)
        self._repo = self._github.get_repo(project)

    def run(self):
        country = prompt_utils.ask_choices(
            "Which country do you want to run the job on?",
            self._countries,
        )

        if not _has_job_pipeline(self._drone, country, self._environment):
            logger.error(
                "There is no job pipeline for the specified country/environment"
            )
            sys.exit(1)

        command = prompt_utils.ask_questions_input(
            "What command do you want to execute?", f"/app/bin/{self._project} "
        )

        self._start_job(country, command)

    def _start_job(self, country, command):
        if self._environment == "staging":
            build = self._get_latest_master_build()

            self._ask_confirm(
                country,
                command,
                f'Current master: {build["message"]} (#{build["number"]})',
            )

            promotion = self._drone.promote_staging(
                build["number"],
                f"job-{country}-{self._environment}",
                f"BATCH_COMMAND={command}&JOB_CPU={self._cpu_request}&JOB_MEMORY={self._memory_request}",
            )
        elif self._environment == "production":
            version = self._get_latest_tag(country)

            self._ask_confirm(country, command, f"Current tag: {version}")

            promotion = self._drone.promote_production(
                version,
                f"job-{country}-{self._environment}",
                f"DRONE_TAG={version}&BATCH_COMMAND={command}&JOB_CPU={self._cpu_request}&JOB_MEMORY={self._memory_request}",
            )

        if "number" not in promotion:
            logger.warning(f"Unable to promote drone build. Response: {promotion}")
            return

        logger.info("Drone build started successfully!")
        logger.info(
            f"You can follow the build status here: {self._drone.get_build_url(promotion['number'])}"
        )

    def _get_latest_master_build(self):
        try:
            builds = self._drone.get_builds_from_branch("master")

            latest_build = None
            non_green_builds = []
            for b in builds:
                if b["status"] == "success":
                    if latest_build is None:
                        latest_build = b
                    break

                non_green_builds.append(b)

            if len(non_green_builds) > 0:
                logger.warning(
                    "There are recent builds on master still running or failed"
                )
                for b in non_green_builds:
                    logger.warning(
                        f'* {b["message"]} (Status: {b["status"]}, Number: #{b["number"]})'
                    )

            if not latest_build:
                logger.error("Unable to find latest build on master")
                sys.exit(255)

            return latest_build

        except Exception as e:
            print(e)
            logger.error(
                "An error has occured retrieving current master version during batch job.\nPlease ask #team-devops for help."
            )
            sys.exit(255)

    def _get_latest_tag(self, country):
        try:
            logger.info("Retrieving latest version, this may take some time...")
            # get latest 10 tags
            tags = self._github.get_tags(self._project)
            #  exclude tags that don't match semver notation
            semver_tags = [t for t in tags if semver.VersionInfo.isvalid(t.name)][0:9]

            builds = []
            for tag in semver_tags:
                for b in self._drone.get_builds_from_tag(tag.name):
                    if (
                        b["event"] == "promote"
                        and b["status"] == "success"
                        and b["deploy_to"] == f"deploy-{country}-production"
                        and "params" in b
                        and "DRONE_TAG" in b["params"]
                    ):
                        builds.append(b)

            if not builds:
                # may end up here if there isn't any successfull build for latest 10 tags
                logger.error(
                    "An error has occured retrieving current version during rollback.\nPlease ask #team-devops for help."
                )
                sys.exit(255)

            # get latest build using build number as key
            current_build = max(builds, key=lambda x: x["number"])

            if not current_build:
                logger.error(
                    f"Unable to determine current version for country {country}"
                )
                sys.exit(255)

            v = semver.VersionInfo.parse(current_build["params"]["DRONE_TAG"])
            logger.info(f"Current version for country {country}: {v}")

            return v
        except Exception as e:
            print(e)
            logger.error(
                "An error has occured retrieving current version during batch job.\nPlease ask #team-devops for help."
            )
            sys.exit(255)

    def _ask_confirm(self, country, command, message):
        logger.info(
            textwrap.dedent(
                f"""
                You're about to run a batch job on project {self._project}, for env {self._environment}, in country {country}.
                {message}
                Command: {command}
                """
            )
        )

        if not prompt_utils.ask_confirm("Do you confirm?", default=False):
            sys.exit(0)


def _parse_available_countries(drone):
    pipelines = drone.parse_yaml()

    if pipelines is None:
        logger.error("The file .drone.yml was not found. Unable to continue.")
        sys.exit(1)

    countries = []
    REGEX = re.compile(r"deploy-([a-z]+)-.*")
    for pipeline in pipelines:
        if "name" in pipeline:
            c = REGEX.findall(pipeline["name"])
            if len(c) > 0 and c[0] is not None and c[0] not in countries:
                countries.append(c[0])

    return countries


def _has_job_pipeline(drone, country, environment):
    pipelines = drone.parse_yaml()

    if pipelines is None:
        logger.error("The file .drone.yml was not found. Unable to continue.")
        sys.exit(1)

    job_pipeline = f"job-{country}-{environment}"
    for pipeline in pipelines:
        if "name" in pipeline and pipeline["name"] == job_pipeline:
            return True

    return False
