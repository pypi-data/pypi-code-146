# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import logging
import pathlib
import re
import subprocess

from .version import version_str

from .job import (
    all_job_variables,
    expand_variables,
)

logger = logging.getLogger(__file__)

DOCKERFILE = (
    "FROM {base_image}\n"
    "COPY runner.toml /etc/gitlab-runner/runner.toml\n"
    "COPY job.json /etc/gitlab-runner/job.json\n"
    'ENV DEBUG="true"\n'
    'ENTRYPOINT ["/usr/bin/gitlab-runner", "exec-fetched-job", '
    '"--config", "/etc/gitlab-runner/runner.toml",'
    '"/etc/gitlab-runner/job.json"]\n'
)

DOCKER_HUB_DOMAIN = 'docker.io'
LEGACY_DOCKER_HUB_DOMAIN = 'index.docker.io'
DOCKER_HUB_OFFICIAL_NAMESPACE = 'library'
DOT_COLON_RX = re.compile(r'[.:]')


def split_docker_image_domain(image_name):
    """Split the name of a Docker image into domain and remainder.

    The image name may include a tag part or not.

    The domain part is normalized to :const:`DOCKER_HUB_DOMAIN`
    if from Docker Hub.

    Reference `Golang implementation <https://github.com/distribution/distribution/blob/main/reference/normalize.go#L87>`_::

        func splitDockerDomain(name string) (domain, remainder string) {
                i := strings.IndexRune(name, '/')
                if i == -1 || (!strings.ContainsAny(name[:i], ".:") && name[:i] != "localhost" && strings.ToLower(name[:i]) == name[:i]) {
                        domain, remainder = defaultDomain, name
                } else {
                        domain, remainder = name[:i], name[i+1:]
                }
                if domain == legacyDefaultDomain {
                        domain = defaultDomain
                }
                if domain == defaultDomain && !strings.ContainsRune(remainder, '/') {
                        remainder = officialRepoName + "/" + remainder
                }
                return
        }
    """ # noqa long lines in Golang code
    # style remark: made to follow reference impl as much as possible
    split = image_name.split('/', 1)
    remainder = split[-1]
    domain = None if len(split) == 1 else split[0]

    if domain is None or (DOT_COLON_RX.search(domain) is None
                          and not domain == 'localhost'
                          and domain.lower() == domain):
        domain, remainder = DOCKER_HUB_DOMAIN, image_name
    if domain == LEGACY_DOCKER_HUB_DOMAIN:
        domain = DOCKER_HUB_DOMAIN

    if domain == DOCKER_HUB_DOMAIN and '/' not in remainder:
        remainder = '/'.join((DOCKER_HUB_OFFICIAL_NAMESPACE,
                              remainder))
    return domain, remainder


class DockerBuildHelper:
    """Help constructing a Docker build context to run jobs for Runners.

    Attributes:

    * :attr:`path` path of the Docker build context to create
    * :attr:`git_process_env` is the common environment `dict` passed to
      `git` subprocesses. The default `None` value means to use the main
      process environment, hence in particular the global Git configuration
      of the user running the process. Passing an environment without user
      identifying variables (`USER` etc) leads to no global config being
      applied (often desirable in tests, maybe not for a service)
    * :attr:`git_user_name`, :attr:`git_user_email` are the committer name and
      email of any commit created by this builder.
      If not specified, default ones for the `git` process end up being used,
      typically inferred from environment variables and global Git
      configuration (the latter depending itself ultimately on the environment,
      see also :attr:`git_process_env`)
    """

    base_image = ("registry.heptapod.net:443/heptapod/"
                  "heptapod-runner:" + version_str)

    git_executable = 'git'

    def __init__(self, path,
                 base_image=None,
                 git_process_env=None,
                 git_user_name=None,
                 git_user_email=None):
        self.path = pathlib.Path(path)
        self.git_process_env = git_process_env
        self.git_user_name = git_user_name
        self.git_user_email = git_user_email
        if base_image is not None:
            self.base_image = base_image

    @classmethod
    def from_runner_config(cls, path, config):
        """Instantiate from a Runner configuration

        This takes care directly of common options.
        """
        return cls(path,
                   git_process_env={},
                   git_user_name="Heptapod Paas Runner",
                   git_user_email='paasrunner@heptapod.test',
                   base_image=config.get('heptapod_runner_main_image'),
                   )

    def git(self, *args, **kwargs):
        kwargs.setdefault('env', self.git_process_env)
        kwargs.setdefault('cwd', self.path)
        cmd = [self.git_executable]
        cmd.extend(args)
        return subprocess.check_output(cmd, **kwargs)

    def amend_job(self, job_data):
        self.job_use_dependency_proxy(job_data)

    def job_use_dependency_proxy(self, job_data):
        """Update job_data to use dependency proxy if available.

        The top-level group URL is used by default. If users want specific
        behaviour, they may use the other variable in the job definition.

        Reference: https://docs.gitlab.com/ee/user/packages/dependency_proxy/#authenticate-within-cicd
        """  # noqa long URL
        job_id = job_data['id']
        # TODO replace job_data by a Job class, and perform lazy
        # once-and-for-all parsing of variables.
        job_vars = all_job_variables(job_data)
        proxy_url = job_vars.get('CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX')
        if not proxy_url:
            logger.debug("Job %d: no dependency proxy available",
                         job_id)
            return

        main_image = job_data.get('image')
        if main_image is not None:
            main_image_name = expand_variables(main_image['name'], job_vars)
            domain, remainder = split_docker_image_domain(main_image_name)
            if domain == DOCKER_HUB_DOMAIN:
                main_image['name'] = '/'.join((proxy_url, remainder))

        services = job_data.get('services')
        if services is None:
            return

        logger.debug("Job %d: services before potential dependency "
                     "proxy rewrite %r", job_id, services)
        new_services = []
        for service in services:
            # service definition can be just a string in YaML file
            # but the coordinator normalizes it to the mapping with
            # name (image/tag), alias, entrypoint etc.
            srv_image_name = service.get('name')
            if srv_image_name is None:
                logger.warning("Job %d: did not understand image/tag "
                               "in service definition %r",
                               job_id, service)
            else:
                expanded_srv = expand_variables(srv_image_name, job_vars)
                srv_domain, srv_remainder = split_docker_image_domain(
                    expanded_srv)

                if srv_domain == DOCKER_HUB_DOMAIN:
                    service['name'] = '/'.join((proxy_url, srv_remainder))
                    # We need to insert an alias so that container linking
                    # works as originally expected by author of the job
                    # configuration (as if we didn't intercept for the
                    # dependency proxy).
                    # For this to work we need to start over from the
                    # original service name, because some normalization that
                    # would change the alias has already occurred with
                    # `srv_remainder` (`postgres` becomes `library/postgres`
                    # giving the `library-postgres` alias).

                    # At this point we are sure that if we have a host part,
                    # it is either `docker.io` or `index.docker.io`, hence
                    # without a port, so the last ':' is guaranteed to
                    # be the tag separator (also deemed 'version' in GitLab
                    # Runner sources).
                    #
                    # Reference for alias value:
                    #  https://docs.gitlab.com/ee/ci/services/#accessing-the-services
                    # We can only put one alias, so we choose the one most
                    # encouraged by GitLab docs, which is compliant with
                    # valid DNS names, aka RFC 1123 section 2.1, itself relying
                    # on RFC 952. TODO document
                    if not service.get('alias'):  # could be empty string
                        # presumably, if there is a user-defined alias, it must
                        # be in use. TODO document
                        service['alias'] = (expanded_srv.rsplit(':', 1)[0]
                                            .replace('/', '-'))
            new_services.append(service)

        job_data['services'] = new_services
        logger.debug("Job %d: services after potential dependency "
                     "proxy rewrite %r", job_id, new_services)

    def write_build_context(self, runner, job_data):
        # TODO transmit concurrency information (necessary for local
        # Docker, and more accurate job logs such as
        # "Running on runnder-TOKEN-project-ID-concurrent-NB")
        runner.dump_inner_config(self.path / 'runner.toml')
        self.amend_job(job_data)
        with (self.path / 'job.json').open('w') as jsonf:
            json.dump(job_data, jsonf)
        (self.path / 'Dockerfile').write_text(
            DOCKERFILE.format(base_image=self.base_image))

    def git_push(self, url):
        """Make the Docker context a Git repository, commit and push."""
        self.git('init', '-q')
        if self.git_user_name:
            self.git('config', 'user.name', self.git_user_name)
        if self.git_user_email:
            self.git('config', 'user.email', self.git_user_email)

        self.git('add', '.')
        self.git('commit', '-m', 'Job definition')
        self.git('remote', 'add', 'clever', url)
        self.git('push', '-q', '--set-upstream', 'clever', 'master')
