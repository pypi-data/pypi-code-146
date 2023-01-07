#!/usr/bin/env python3

import argparse
import logging
import re
import requests
import sh
import shutil
import sys
import tempfile
import time
from furl import furl
from bs4 import BeautifulSoup
from dataclasses import dataclass
from functools import wraps

logging.basicConfig()
logger = logging.getLogger(__name__)


class RetryException(Exception):
    pass


def retry(exceptions, tries=2, delay=1):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries + 1, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.info('%s: %s, Retrying in %s seconds...', f.__qualname__, e, mdelay)
                    if mtries == tries + 1:
                        logger.debug("", exc_info=True)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= 2
            raise RetryException("Number of retries exceeded for function " + f.__name__)
        return f_retry
    return deco_retry


class Gitea(object):
    def __init__(self, hostname):
        self._hostname = hostname
        self._url = f'https://{hostname}'
        self._users = self.users_factory()(self)
        self._projects = self.projects_factory()(self)
        self._s = requests.Session()

    @property
    def hostname(self):
        return self._hostname

    @property
    def url(self):
        return self._url

    @property
    def projects(self):
        return self._projects

    @property
    def users(self):
        return self._users

    @property
    def s(self):
        return self._s

    def certs(self, certs):
        self.s.verify = certs
        return self

    def authenticate(self, **kwargs):
        self._session()
        self.login(kwargs["username"], kwargs["password"])
        self._user = self.s.get(f"{self.s.api}/user").json()

    @property
    def is_authenticated(self):
        return hasattr(self, "_user")

    @property
    def username(self):
        return self._user["login"]

    @property
    def is_admin(self):
        return self._user["is_admin"]

    def _session(self):
        self.s.api = f"{self.url}/api/v1"

    def login(self, username, password):
        self.password = password
        r = self.s.post(
            f"{self.s.api}/users/{username}/tokens",
            auth=(username, password),
            json={
                "name": f"TEST{time.time()}",
            },
        )
        r.raise_for_status()
        self.set_token(r.json())

    def logout(self):
        self.delete_token()
        if self.is_authenticated:
            del self._user

    def set_token(self, token):
        self.token = token
        self.s.headers["Authorization"] = f"token {self.token['sha1']}"

    def get_token(self):
        return self.token['sha1']

    def delete_token(self):
        if hasattr(self, 'token'):
            r = self.s.delete(
                f"{self.s.api}/users/{self.username}/tokens/{self.token['id']}",
                auth=(self.username, self.password),
            )
            r.raise_for_status()
            del self.token
            return True
        else:
            return False

    def projects_factory(self):
        return GiteaProjects

    def users_factory(self):
        return GiteaUsers


class GiteaUsers(object):
    def __init__(self, forge):
        self._forge = forge

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    def get(self, username):
        if username == self.forge.username:
            r = self.s.get(f"{self.s.api}/user")
        elif self.forge.is_admin:
            r = self.s.get(f"{self.s.api}/user", params={"sudo": username})
        else:
            r = self.s.get(f"{self.s.api}/users/{username}")
        if r.status_code == 404:
            return None
        else:
            r.raise_for_status()
            return GiteaUser(self.forge, r.json())

    def delete(self, username):
        user = self.get(username)
        if user is None:
            return False
        while True:
            r = self.s.delete(f"{self.s.api}/admin/users/{username}")
            if r.status_code == 404:
                break
            if r.status_code != 204:
                logger.error(f"{r.status_code}: {r.text}")
            logger.debug(r.text)
            r.raise_for_status()
        return True

    def create(self, username, password, email, **data):
        # the API does not support creating an admin user
        assert data.get("admin") is not True, "Creating an admin user with Gitea is not implemented"
        info = self.get(username)
        if info is None:
            r = self.s.post(
                f"{self.s.api}/admin/users",
                data={
                    "username": username,
                    "email": email,
                    "password": password,
                },
            )
            if r.status_code != 201:
                logger.error(r.text)
            r.raise_for_status()
            info = r.json()
            Gitea(self.forge.hostname).certs(self.s.verify).users._finalize_user_create(
                username, password)
            info = self.get(username)
        return info

    def _finalize_user_create(self, username, password):
        r = self.s.post(
            f"{self.forge.url}/user/login",
            data={
                "user_name": username,
                "password": password,
            },
        )
        r.raise_for_status()
        r = self.s.post(
            f"{self.forge.url}/user/settings/change_password",
            data={
                "password": password,
                "retype": password,
                "_csrf": self.s.cookies["_csrf"],
            },
        )
        r.raise_for_status()

    def list(self):
        r = self.s.get(f"{self.s.api}/users/search")
        r.raise_for_status()
        j = r.json()
        assert j["ok"]
        for u in j["data"]:
            yield GiteaUser(self.forge, u)


class GiteaUser(object):
    def __init__(self, forge, user):
        self._forge = forge
        self._user = user

    @property
    def url(self):
        return f"{self.forge.url}/{self.username}"

    @property
    def username(self):
        return self._user["username"]

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    def __eq__(self, other):
        return (
            isinstance(other, GiteaUser)
            and self.forge == other.forge
            and self.url == other.url
            and self.username == other.username
        )

    def get_keys(self):
        r = self.s.get(f"{self.s.api}/user/keys")
        r.raise_for_status()
        return r.json()

    def get_key(self, title):
        for key in self.get_keys():
            if key["title"] == title:
                return key
        return None

    def delete_key(self, title):
        key = self.get_key(title)
        if key:
            r = self.s.delete(f"{self.s.api}/user/keys/{key['id']}")
            r.raise_for_status()

    def create_key(self, title, key):
        data = {
            "title": title,
            "key": key,
        }
        r = self.s.post(f"{self.s.api}/user/keys", data=data)
        logger.debug(r.text)
        r.raise_for_status()

    def get_applications(self):
        r = self.s.get(f"{self.s.api}/user/applications/oauth2")
        r.raise_for_status()
        return r.json()

    def get_application(self, name):
        for app in self.get_applications():
            if app["name"] == name:
                return app
        return None

    def delete_application(self, name):
        app = self.get_application(name)
        if app:
            r = self.s.delete(f"{self.s.api}/user/applications/oauth2/{app['id']}")
            r.raise_for_status()
        return app

    def create_application(self, name, redirect_uri):
        app = self.get_application(name)
        if app is None:
            data = {
                "name": name,
                "redirect_uris": [redirect_uri],
            }
            r = self.s.post(f"{self.s.api}/user/applications/oauth2", json=data)
            r.raise_for_status()
            app = self.get_application(name)
        return app

    @property
    def projects(self):
        params = {"uid": self._user["id"]}
        projects = self.s.get(f"{self.s.api}/repos/search", params=params)
        projects.raise_for_status()
        raw = projects.json()
        assert raw["ok"]
        for project in raw["data"]:
            yield GiteaProject(self.forge, project)


class GiteaProjects(object):
    def __init__(self, forge):
        self._forge = forge

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    def project_factory(self):
        return GiteaProject

    def get(self, namespace, project):
        r = self.s.get(f"{self.s.api}/repos/{namespace}/{project}")
        if r.status_code == requests.codes.ok:
            return self.project_factory()(self.forge, r.json())
        else:
            return None

    class DeletionInProgress(Exception):
        pass

    @retry(DeletionInProgress, tries=5)
    def _create(self, namespace, project, **data):
        data.update(
            {
                "name": project,
            }
        )
        r = self.s.post(f"{self.s.api}/user/repos", data=data)
        logger.debug(r.text)
        if r.status_code == 201:
            return self.get(namespace, project)
        r.raise_for_status()

    def create(self, namespace, project, **data):
        p = self.get(namespace, project)
        if p is None:
            return self._create(namespace, project, **data)
        else:
            return p

    def delete(self, namespace, project):
        p = self.get(namespace, project)
        if p is None:
            return False
        r = self.s.delete(f"{self.s.api}/repos/{namespace}/{project}")
        r.raise_for_status()
        while self.get(namespace, project) is not None:
            time.sleep(1)
        return True

    def list(self):
        projects = self.s.get(f"{self.s.api}/repos/search")
        projects.raise_for_status()
        raw = projects.json()
        assert raw["ok"]
        for project in raw["data"]:
            yield GiteaProject(self.forge, project)


class GiteaProject(object):
    def __init__(self, forge, project):
        self._forge = forge
        self._project = project
        self._keys = GiteaProjectKeys(self)

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    @property
    def id(self):
        return self._project["id"]

    @property
    def namespace(self):
        return self._project["owner"]["login"]

    @property
    def project(self):
        return self._project["name"]

    @property
    def keys(self):
        return self._keys

    @property
    def ssh_url_to_repo(self):
        return self._project["ssh_url"]

    @property
    def http_url_to_repo(self):
        return self._project["clone_url"]

    @property
    def http_url_to_repo_with_auth(self):
        o = furl(self.http_url_to_repo)
        o.username = self.forge.username
        o.password = self.forge.get_token()
        return o.tostr()

    def get_applications(self):
        r = self.s.get(f"{self.s.api}/user/applications/oauth2")
        r.raise_for_status()
        return r.json()

    def __eq__(self, other):
        return (
            isinstance(other, GiteaProject)
            and self.id == other.id
            and self.namespace == other.namespace
            and self.project == other.project
            and self.http_url_to_repo == other.http_url_to_repo
            and self.ssh_url_to_repo == other.ssh_url_to_repo
        )


class GiteaProjectKeys(object):
    def __init__(self, project):
        self._project = project

    @property
    def project(self):
        return self._project

    @property
    def s(self):
        return self.project.s

    def _build_url(self):
        return f"{self.s.api}/repos/{self.project.namespace}/{self.project.project}/keys"

    def get(self, id):
        response = self.s.get(f"{self._build_url()}/{int(id)}")  # ensure id is not None
        if response.status_code == 404:
            return None
        else:
            response.raise_for_status()
            return GiteaProjectKey(self.project, response.json())

    def delete(self, id):
        p = self.get(id)
        if p is None:
            return False
        r = self.s.delete(f"{self._build_url()}/{id}")
        r.raise_for_status()
        return True

    def _create(self, title, key, read_only):
        data = {
            "title": title,
            "key": key,
            "read_only": read_only,
        }
        response = self.s.post(f"{self._build_url()}", data=data)
        logger.info(response.text)
        if response.status_code == 201:
            key = response.json()
            return self.get(key["id"])
        response.raise_for_status()

    def create(self, title, key, read_only):
        for k in self.list():
            if k.key == key:
                return k
        return self._create(title, key, read_only)

    def list(self):
        response = self.s.get(f"{self._build_url()}")
        response.raise_for_status()
        for key in response.json():
            yield GiteaProjectKey(self.project, key)


class GiteaProjectKey(object):
    def __init__(self, project, key):
        self._project = project
        self._key = key

    @property
    def project(self):
        return self._project

    @property
    def id(self):
        return self._key["id"]

    @property
    def key(self):
        return self._key["key"]

    @property
    def title(self):
        return self._key["title"]

    def __eq__(self, other):
        return (
            isinstance(other, GiteaProjectKey)
            and self.id == other.id
            and self.title == other.title
        )


class GiteaBrowser(object):

    def __init__(self, hostname, user, password, certs):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.certs = certs

    def login(self):
        #
        # This is **different** from Gitea.authenticate() which
        # obtains a token for API interactions. It is limited to
        # simulating user browsing.
        #
        #
        # Gitea home page
        #
        self.g = requests.Session()
        self.g.verify = self.certs
        self.g.url = f'https://{self.hostname}'
        r = self.g.get(self.g.url + '/user/login')
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.select(
            'form[action="/user/login"] input[name="_csrf"]')[0]['value']

        #
        # Gitea Login
        #
        r = self.g.post(self.g.url + '/user/login', data={
            '_csrf': csrf,
            'user_name': self.user,
            'password': self.password,
        })
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        error = soup.select('.flash-error')
        if error:
            raise Exception(f'login {self.user}: {error}')

    def revoke_application(self, name):
        #
        # Revoke woodpecker application
        #
        r = self.g.get(self.g.url + '/user/settings/applications')
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.select(
            'form[action="/user/settings/applications"] input[name="_csrf"]')[0]['value']
        revoked = []
        for b in soup.select('button[data-modal-id="revoke-gitea-oauth2-grant"]'):
            found = b.parent.parent.select('.content strong')
            assert len(found) >= 1, f"{b} does not have the expected structure"

            if f'>{name}<' not in str(found[0]):
                logger.info(f"{found[0]} does not contain {name}, skipping")
                continue

            id = b["data-id"]
            data = {
                "id": id,
                '_csrf': csrf,
            }
            logger.info(f"revoking grant id {id} for application {name}")
            r = self.g.post(self.g.url + "/user/settings/applications/oauth2/revoke",
                            data=data)
            r.raise_for_status()
            revoked.append(id)
        return revoked

    def confirm_oauth(self, url, redirect):
        logger.info(f"confirm oauth {url} redirect {redirect}")
        r = self.g.get(url,
                       allow_redirects=False)
        r.raise_for_status()
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            data = {
                "redirect_uri": redirect,
            }
            for input in soup.select('form[action="/login/oauth/grant"] input[type="hidden"]'):
                if (
                        input.get('name') is None or
                        input.get('value') is None or
                        input.get('value') == ''
                ):
                    continue
                logger.info(f"collected hidden input {input['name']} {input['value']}")
                data[input['name']] = input['value']
            assert len(data) > 1, f"{data} has only one field, more are expected"
            r = self.g.post(self.g.url + '/login/oauth/grant', data=data,
                            allow_redirects=False)
            r.raise_for_status()
            logger.info("oauth confirmed")
        elif r.status_code == 302:
            logger.info("no confirmation required")
        location = r.headers['Location']
        logger.info(f"going back to {location}")
        assert location.startswith(redirect)
        return location


class Woodpecker(object):
    #
    # The API is undocumented and must be read from woodpecker/server/router/api.go
    #

    def __init__(self, gitea_browser, gitea_user, hostname, certs):
        self.gitea_browser = gitea_browser
        self.gitea_user = gitea_user
        self.hostname = hostname
        self.certs = certs

    def login(self):
        self.w = requests.Session()
        self.w.verify = self.certs
        self.w.url = f'https://{self.hostname}'
        r = self.w.get(self.w.url + '/authorize',
                       allow_redirects=False)
        r.raise_for_status()
        #
        # Gitea OAuth confirmation page
        #
        location = self.gitea_browser.confirm_oauth(
            r.headers['Location'],
            f"https://{self.hostname}/authorize")
        r = self.w.get(location, allow_redirects=False)
        r.raise_for_status()

        #
        # Woodpecker CSRF
        #
        r = self.w.get(self.w.url + '/web-config.js',
                       allow_redirects=False)
        r.raise_for_status()
        csrf = re.findall('window.WOODPECKER_CSRF = "(.*?)"', r.text)[0]

        #
        # Woodpecker token
        #
        r = self.w.post(self.w.url + '/api/user/token',
                        headers={'X-CSRF-TOKEN': csrf},
                        allow_redirects=False)
        r.raise_for_status()
        self.token = r.text
        self.w.headers = {'Authorization': f'Bearer {self.token}'}

    def refresh(self):
        self.w.get(self.w.url + "/api/user/repos?all=true&flush=true").raise_for_status()

    def build_logs(self, project, sha, step):
        url = self.w.url + f"/api/repos/{self.gitea_user}/{project}"

        @retry(AssertionError, tries=4)
        def wait_for_build():
            r = self.w.get(f"{url}/builds")
            r.raise_for_status()
            for build in r.json():
                if build['commit'] == sha:
                    return build['number']
            assert 0, f"build with commit {sha} not found in {r.text}"
        number = wait_for_build()
        r = self.w.get(f"{url}/builds/{number}")
        r.raise_for_status()

        def get_pid(children):
            for proc in children:
                if proc["name"] == step:
                    return proc["pid"]
            raise Exception(f"no children named {proc['name']} in {children}")
        pid = get_pid(r.json()["procs"][0]["children"])

        @retry(AssertionError, tries=4)
        def wait_for_logs():
            u = f"{url}/logs/{number}/{pid}"
            r = self.w.get(u)
            if r.status_code == 404:
                assert 0, f"no logs yet for {u}"
            r.raise_for_status()
            return r.text
        log = wait_for_logs()
        logger.debug(log)
        return log

    def disable_project(self, project):
        self.refresh()
        r = self.w.get(self.w.url + f"/api/repos/{self.gitea_user}/{project}")
        r.raise_for_status()
        logger.info(f"disable project {project} {r.text}")
        if r.json()['active'] is False:
            return False
        self.w.delete(self.w.url + f"/api/repos/{self.gitea_user}/{project}").raise_for_status()
        return True

    def enable_project(self, project):
        self.refresh()
        r = self.w.get(self.w.url + f"/api/repos/{self.gitea_user}/{project}")
        r.raise_for_status()
        logger.info(f"enabling project {project} {r.text}")
        if r.json()['active'] is True:
            return False
        self.w.post(self.w.url + f"/api/repos/{self.gitea_user}/{project}").raise_for_status()
        self.w.patch(self.w.url + f"/api/repos/{self.gitea_user}/{project}",
                     json={
                         "trusted": True,
                         "visibility": "internal",
                     }).raise_for_status()
        r = self.w.get(self.w.url + f"/api/repos/{self.gitea_user}/{project}")
        r.raise_for_status()
        logger.info(f"enabled project {project} {r.text}")
        return True

    def add_secret(self, project, name, value, events):
        r = self.w.post(self.w.url + f"/api/repos/{self.gitea_user}/{project}/secrets",
                        json={
                            "event": events,
                            "name": name,
                            "value": value,
                        })
        r.raise_for_status()
        logger.info(f"added secret {name} to project {project} {r.text}")
        return True

    def list_secrets(self, project):
        r = self.w.get(self.w.url + f"/api/repos/{self.gitea_user}/{project}/secrets")
        r.raise_for_status()
        for secret in r.json():
            yield secret

    def delete_secret(self, project, name):
        for secret in self.list_secrets(project):
            if secret["name"] == name:
                r = self.w.delete(
                    self.w.url + f"/api/repos/{self.gitea_user}/{project}/secrets/{name}")
                r.raise_for_status()
                logger.info(f"deleted secret {name} from project {project} {r.text}")
                return True
        return False


@dataclass
class Hostea(object):
    certs: str
    gitea_hostname: str
    admin_user: str
    admin_password: str
    user: str
    password: str
    email: str
    project: str
    woodpecker_hostname: str
    deploy: str = None
    woodpecker_token_path: str = None
    enough_api_token: str = None
    verbose: bool = False
    debug: bool = False

    def setup(self):
        self.gitea_create()
        self.gitea_user_create()
        self.gitea_project_create()
        self.gitea_add_deploy()
        self.woodpecker_auth()
        self.woodpecker_save_token()
        self.woodpecker_enable_project()
        self.woodpecker_add_deploy()
        self.woodpecker_add_enough()

    def destroy(self):
        self.gitea_create()
        self.gitea.authenticate(username=self.admin_user, password=self.admin_password)
        if self.gitea.users.get(self.user):
            self.destroy_project()
            self.gitea.users.delete(self.user)
        self.gitea.logout()

    def update_project(self, content_dir):
        self.git_init_project()
        self.git_checkout_project()
        shutil.copytree(content_dir, self.git_directory.name, dirs_exist_ok=True)
        return self.git_push_project()

    def git_push_project(self):
        self.git.add('.')
        self.git.config('user.email', self.email)
        self.git.config('user.name', self.user)
        try:
            self.git.commit('-m', 'hostea: hosteasetup.py update complete')
        except sh.ErrorReturnCode_1:
            logger.debug("no change")
        else:
            self.git.push('origin', 'master')
        sha = self.git('rev-parse', 'origin/master')
        return str(sha).strip()

    def git_checkout_project(self):
        try:
            self.git('ls-remote', '--quiet', '--exit-code', 'origin', 'master')
            self.git.checkout('-b', 'master', 'origin/master')
        except sh.ErrorReturnCode_2:
            logger.debug("repository is empty")

    def git_init_project(self):
        if hasattr(self, 'git'):
            return False
        self.git_directory = tempfile.TemporaryDirectory()
        self.git = sh.git.bake(_cwd=self.git_directory.name)
        self.git.init()

        p = self.gitea.projects.get(self.user, self.project)
        url = p.http_url_to_repo_with_auth
        self.git.config('http.sslVerify', 'false')
        self.git.remote.add.origin(url)
        self.git.fetch()
        return True

    def destroy_project(self):
        self.woodpecker_auth()
        self.woodpecker_disable_project()
        self.gitea_browser.revoke_application("woodpecker")
        self.gitea.projects.delete(self.user, self.project)

    def gitea_create(self):
        self.gitea = Gitea(self.gitea_hostname)
        self.gitea.certs(self.certs)

    def gitea_user_create(self):
        self.gitea.authenticate(username=self.admin_user, password=self.admin_password)
        self.gitea.users.create(self.user, self.password, self.email)
        self.gitea.authenticate(username=self.user, password=self.password)

    def gitea_project_create(self):
        return self.gitea.projects.create(self.user, self.project, private=True)

    def gitea_add_deploy(self):
        return self.gitea.projects.get(self.user, self.project).keys.create(
            title="deploy",
            key=open(f"{self.deploy}.pub").read().strip(),
            read_only=False)

    def woodpecker_auth(self):
        self.gitea_browser = GiteaBrowser(
            self.gitea_hostname, self.user, self.password, self.certs)
        self.gitea_browser.login()
        self.woodpecker = Woodpecker(
            self.gitea_browser, self.user, self.woodpecker_hostname, self.certs)
        self.woodpecker.login()

    def woodpecker_save_token(self):
        if not self.woodpecker_token_path:
            return False
        open(self.woodpecker_token_path, "w").write(self.woodpecker.token)
        sh.chmod("400", self.woodpecker_token_path)
        return True

    def woodpecker_enable_project(self):
        return self.woodpecker.enable_project(self.project)

    def woodpecker_add_deploy(self):
        self.woodpecker.delete_secret(self.project, "deploy")
        return self.woodpecker.add_secret(
            self.project, "deploy", open(self.deploy).read().strip(), ["push"])

    def woodpecker_add_enough(self):
        if not self.enough_api_token:
            return None
        self.woodpecker.delete_secret(self.project, "enough")
        return self.woodpecker.add_secret(
            self.project, "enough", self.enough_api_token, ["push"])

    def woodpecker_disable_project(self):
        return self.woodpecker.disable_project(self.project)


def main(argv):
    parser = argparse.ArgumentParser(description='Hostea setup.')
    parser.add_argument('--enough-api-token', help='set to a domain, for testing')
    parser.add_argument('--deploy', help='path to the private deploy key')
    parser.add_argument('--woodpecker-token-path', help='path to save the woodpecker token')
    parser.add_argument('--certs', help='directory with certificate authorities')
    parser.add_argument('--verbose', action='store_true', help='verbose output')
    parser.add_argument('--debug', action='store_true', help='debug output')
    parser.add_argument(
        '--update-directory',
        help='update the project repository with the content of this directory')
    parser.add_argument('gitea_hostname')
    parser.add_argument('admin_user')
    parser.add_argument('admin_password')
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('email')
    parser.add_argument('project')
    parser.add_argument('woodpecker_hostname')
    args = parser.parse_args(argv)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(logging.INFO)

    d = vars(args)
    update_directory = d['update_directory']
    del d['update_directory']
    hostea = Hostea(**d)
    hostea.setup()
    if update_directory:
        hostea.update_project(update_directory)
    return (hostea.gitea, hostea.woodpecker)


if __name__ == '__main__':
    main(sys.argv[1:])
