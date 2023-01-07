import os
from urllib.parse import urlunparse, urlparse
from html.parser import HTMLParser
from time import sleep

from requests import Session
import requests

from .csrf import ParseCSRF

# GITEA_USER = "root"
# GITEA_EMAIL = "root@example.com"
# GITEA_PASSWORD = "foobarpassword"
# HOST = "http://localhost:8080"
#
# REPOS = []


class Gitea:
    def __init__(self, host: str, username: str, password: str, email: str, c: Session):
        self.host = host
        self.username = username
        self.password = password
        self.email = email
        self.c = c
        self.__csrf_key = "_csrf"
        self.__logged_in = False

    def get_uri(self, path: str):
        parsed = urlparse(self.host)
        return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))

    def get_api_uri(self, path: str):
        parsed = urlparse(self.host)
        return urlunparse(
            (
                parsed.scheme,
                f"{self.username}:{self.password}@{parsed.netloc}",
                path,
                "",
                "",
                "",
            )
        )

    @staticmethod
    def check_online(host: str):
        """
        Check if Gitea instance is online
        """
        count = 0
        parsed = urlparse(host)
        url = urlunparse((parsed.scheme, parsed.netloc, "api/v1/nodeinfo", "", "", ""))

        while True:
            try:
                res = requests.get(url, allow_redirects=False)
                if any([res.status_code == 302, res.status_code == 200]):
                    break
            except Exception:
                sleep(2)
                print(f"Retrying {count} time")
                count += 1
                continue

    def install(self):
        """
        Install Gitea, first form that a user sees when a new instance is
        deployed
        """
        cwd = os.environ.get("PWD")
        user = os.environ.get("USER")
        payload = {
            "db_type": "sqlite3",
            "db_host": "localhost:3306",
            "db_user": "root",
            "db_passwd": "",
            "db_name": "gitea",
            "ssl_mode": "disable",
            "db_schema": "",
            "charset": "utf8",
            "db_path": f"{cwd}/tmp/gitea/db/gitea.db",
            "app_name": "Gitea:+Git+with+a+cup+of+tea",
            "repo_root_path": f"{cwd}/tmp/gitea/repos/",
            "lfs_root_path": f"{cwd}/tmp/gitea/lfs/",
            "run_user": user,
            "domain": "localhost",
            "ssh_port": "2222",
            "http_port": "3000",
            "app_url": self.get_uri(""),
            "log_root_path": f"{cwd}/tmp/gitea/log/",
            "smtp_host": "",
            "smtp_from": "",
            "smtp_user": "",
            "smtp_passwd": "",
            "enable_federated_avatar": "on",
            "enable_open_id_sign_in": "on",
            "enable_open_id_sign_up": "on",
            "default_allow_create_organization": "on",
            "default_enable_timetracking": "on",
            "no_reply_address": "noreply.localhost",
            "password_algorithm": "pbkdf2",
            "admin_name": "",
            "admin_passwd": "",
            "admin_confirm_passwd": "",
            "admin_email": "",
        }

        self.c.post(self.get_uri(""), data=payload)
        sleep(10)

    def get_csrf_token(self, url: str) -> str:
        """
        Get CSRF token at a URI
        """
        resp = self.c.get(url, allow_redirects=False)
        if resp.status_code != 200 and resp.status_code != 302:
            print(resp.status_code, resp.text)
            raise Exception(f"Can't get csrf token: {resp.status_code}")
        parser = ParseCSRF(name=self.__csrf_key)
        parser.feed(resp.text)
        csrf = parser.token
        return csrf

    def register(self):
        """
        Register User
        """
        url = self.get_uri("/user/sign_up")
        csrf = self.get_csrf_token(url)
        payload = {
            "_csrf": csrf,
            "user_name": self.username,
            "password": self.password,
            "retype": self.password,
            "email": self.email,
        }
        self.c.post(url, data=payload, allow_redirects=False)

    def login(self):
        """
        Login, must be called at least once before performing authenticated
        operations
        """
        if self.__logged_in:
            return
        url = self.get_uri("/user/login")
        csrf = self.get_csrf_token(url)
        payload = {
            "_csrf": csrf,
            "user_name": self.username,
            "password": self.password,
            "remember": "on",
        }
        resp = self.c.post(url, data=payload, allow_redirects=False)
        if any(
            [resp.status_code == 302, resp.status_code == 200, resp.status_code == 303]
        ):
            print("User logged in")
            self.__logged_in = True
            return

        raise Exception(
            f"[ERROR] Authentication failed. status code {resp.status_code}"
        )

    def create_repository(self, name: str):
        """
        Create repository
        """
        self.login()

        def get_repository_payload(csrf: str, name: str, user_id: str):
            data = {
                "_csrf": csrf,
                "uid": user_id,
                "repo_name": name,
                "description": f"this repository is named {name}",
                "repo_template": "",
                "issue_labels": "",
                "gitignores": "",
                "license": "",
                "readme": "Default",
                "default_branch": "master",
                "trust_model": "default",
            }
            return data

        url = self.get_uri("/repo/create")
        user_id = self.c.get(self.get_api_uri("/api/v1/user")).json()["id"]

        csrf = self.get_csrf_token(url)
        data = get_repository_payload(csrf, name, user_id=user_id)

        resp = self.c.post(url, data=data, allow_redirects=False)
        print(f"Created repository {name}")
        if resp.status_code != 302 and resp.status_code != 200:
            raise Exception(
                f"Error while creating repository: {name} {resp.status_code}"
            )

    def install_sso(
        self,
        sso_name: str,
        client_id: str,
        client_secret: str,
        sso_auto_discovery_url: str,
    ):
        self.login()
        """
        Install SSO.

        - sso_name: human readable SSO name. Doesn't have any functionality
        except assisting admins ID an SSO by a name

        - client_id: OAuth stuff, will be generated by the SSO that should be integrated

        - client_secret: OAuth stuff, will be generated by the SSO that should be integrated

        - sso_auto_discovery_url: Again OAuth stuff. Should be available in the SSO documentation.
          In Hostea SSO's case, it is available at
          https://hostea-dash.example.org/o/.well-known/openid-configuration/
        """
        csrf = self.get_csrf_token(self.get_uri("/admin/auths/new"))
        payload = {
            "_autofill_dummy_username": "",
            "_autofill_dummy_password": "",
            "_csrf": csrf,
            "type": "6",
            "name": sso_name,
            "security_protocol": "",
            "host": "",
            "port": "",
            "bind_dn": "",
            "bind_password": "",
            "user_base": "",
            "user_dn": "",
            "filter": "",
            "admin_filter": ["", ""],
            "attribute_username": "",
            "attribute_name": "",
            "attribute_surname": "",
            "attribute_mail": "",
            "attribute_ssh_public_key": "",
            "attribute_avatar": "",
            "group_dn": "",
            "group_member_uid": "",
            "user_uid": "",
            "group_filter": "",
            "group_team_map": "",
            "search_page_size": "",
            "smtp_auth": "PLAIN",
            "smtp_host": "",
            "smtp_port": "",
            "helo_hostname": "",
            "allowed_domains": "",
            "pam_service_name": "",
            "pam_email_domain": "",
            "oauth2_provider": "openidConnect",
            "oauth2_key": client_id,
            "oauth2_secret": client_secret,
            "oauth2_icon_url": "",
            "open_id_connect_auto_discovery_url": sso_auto_discovery_url,
            "oauth2_auth_url": "",
            "oauth2_token_url": "",
            "oauth2_profile_url": "",
            "oauth2_email_url": "",
            "oauth2_tenant": "",
            "oauth2_scopes": "openid",
            "oauth2_required_claim_name": "",
            "oauth2_required_claim_value": "",
            "oauth2_group_claim_name": "",
            "oauth2_admin_group": "",
            "oauth2_restricted_group": "",
            "sspi_auto_create_users": "on",
            "sspi_auto_activate_users": "on",
            "sspi_strip_domain_names": "on",
            "sspi_separator_replacement": "_",
            "sspi_default_language": "",
            "is_sync_enabled": "on",
            "is_active": "on",
        }

        self.c.post(self.get_uri("/admin/auths/new"), data=payload)


class ParseSSOLogin(HTMLParser):
    url: str = None

    def handle_starttag(self, tag: str, attrs: (str, str)):
        if self.url:
            return

        if tag != "a":
            return

        for (index, (k, v)) in enumerate(attrs):
            if k == "href":
                if "/user/oauth2/" in v:
                    self.url = v
                    return


class GiteaSSO:
    def __init__(
        self,
        username: str,
        email: str,
        gitea_host: str,
        hostea_org: str,
        support_repo: str,
        c: Session,
    ):
        self.c = c
        self.username = username
        self.gitea_host = gitea_host
        self.hostea_org = hostea_org
        self.support_repo = support_repo
        self.email = email

        self.__csrf_key = "_csrf"

        url = urlparse(self.gitea_host)
        repo = f"{self.hostea_org}/{self.support_repo}"
        issues = f"{repo}/issues"
        new_issues = f"{issues}/new"

        self.__partial_call_back_url = urlunparse(
            (url.scheme, url.netloc, "/user/oauth2/", "", "", "")
        )
        self.__login = urlunparse((url.scheme, url.netloc, "/user/login/", "", "", ""))
        self.__link_acount = urlunparse(
            (url.scheme, url.netloc, "/user/link_account/", "", "", "")
        )
        self.__link_acount_signup = urlunparse(
            (url.scheme, url.netloc, "/user/link_account_signup/", "", "", "")
        )

        self.__me = urlunparse(
            (url.scheme, url.netloc, f"/{self.username}", "", "", "")
        )

        self.issues_uri = urlunparse((url.scheme, url.netloc, issues, "", "", ""))
        self.new_issues_uri = urlunparse(
            (url.scheme, url.netloc, new_issues, "", "", "")
        )

    def get_csrf(self, url: str) -> str:
        resp = self.c.get(url)
        parser = ParseCSRF(name=self.__csrf_key)
        parser.feed(resp.text)
        return parser.token

    def _sso_login(self):
        resp = self.c.get(self.__login)
        parser = ParseSSOLogin()
        parser.feed(resp.text)

        url = urlparse(self.gitea_host)
        # SSO URL in Gitea login page
        sso = urlunparse((url.scheme, url.netloc, parser.url, "", "", ""))

        # redirects are enabled to for a cleaner implementation. Commented out
        # code below does the same in a step-by-step manner
        resp = self.c.get(sso)
        resp.raise_for_status()
        assert "Sign In to Authorize Linked Account" in resp.text
