from django.conf import settings
import logging
import os
import requests
import time


logger = logging.getLogger(__name__)


#
# Not using python-gitlab because it does not support /oauth/token
# see https://github.com/python-gitlab/python-gitlab/issues/753
#
#
# https://docs.gitlab.com/ce/api/oauth2.html#resource-owner-password-credentials
#
class GitLab(object):

    def __init__(self, url):
        self.url = url
        self._session()

    def _session(self):
        self.s = requests.Session()
        if 'REQUESTS_CA_BUNDLE' not in os.environ:
            self.s.verify = settings.CERTS_DIR
        self.s.api = self.url + '/api/v4'

    def certs(self, certs):
        self.s.verify = certs

    def login(self, username, password):
        r = self.s.post(self.url + '/oauth/token', json={
            'username': username,
            'password': password,
            'grant_type': 'password',
        })
        r.raise_for_status()
        self.set_token(r.json()['access_token'])

    def set_token(self, token):
        self.s.headers['Authorization'] = f'Bearer {token}'

    def get_namespace(self, user):
        r = self.s.get(self.s.api + '/namespaces?search=' + user)
        r.raise_for_status()
        return r.json()[0]['id']

    def group_members(self, group):
        r = self.s.get(self.s.api + f'/groups/{group}/members')
        r.raise_for_status()
        return r.json()

    def is_member_of_group(self, group, username):
        return any([x['username'] == username for x in self.group_members(group)])

    def is_self_member_of_group(self, group):
        r = self.s.get(self.s.api + '/user')
        r.raise_for_status()
        user = r.json()
        return self.is_member_of_group(group, user['username'])

    def recreate_project(self, user, project):
        namespace_id = self.get_namespace(user)
        r = self.s.get(self.s.api + '/projects/' + user + '%2F' + project)
        if r.status_code == requests.codes.ok:
            r = self.s.delete(self.s.api + '/projects/' + user + '%2F' + project)
            r.raise_for_status()
        for _ in range(10):
            r = self.s.post(self.s.api + '/projects', data={
                "name": project,
                "namespace_id": int(namespace_id),
                "visibility": "public",
            })
            time.sleep(5)
            if r.status_code == 201:
                break
            print(str(r.text))
        r.raise_for_status()

    def create_api_application(self, domain):
        callbacks = [
            f'https://api.{domain}/accounts/gitlab/login/callback/',
        ]
        r = self.s.post(self.s.api + '/applications', json={
            'name': 'api',
            'redirect_uri': "\n".join(callbacks),
            'scopes': "api\nread_user",
            })
        logger.debug(r.text)
        r.raise_for_status()
        j = r.json()
        return j['application_id'], j['secret']

    def ensure_group_exists(self, name, **kwargs):
        r = self.s.get(f'{self.s.api}/groups/{name}')
        if r.status_code == 200:
            return
        args = {'name': name, 'path': name}
        args.update(kwargs)
        r = self.s.post(f'{self.s.api}/groups', json=args)
        r.raise_for_status()
