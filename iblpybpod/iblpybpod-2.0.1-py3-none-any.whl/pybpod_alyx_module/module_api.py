from one.webclient import AlyxClient
from confapp import conf


class AlyxModule(object):

    def __init__(self):
        self._addr = conf.ALYX_PLUGIN_ADDRESS
        self._api = None

    def _connect_to_alyx(self, username, password):
        try:
            if self._api is None:
                self._api = AlyxClient(username=username, password=password, base_url=self._addr)
        except Exception:
            return False

        return True

    def get_alyx_subjects(self, username):
        return self._api.rest('subjects', 'list', '?responsible_user={name}'.format(name=username))

    def get_alyx_subject_info(self, nickname):
        return self._api.rest('subjects', 'list', '/{nick}'.format(nick=nickname))

    def set_alyx_address(self, value):
        self._addr = value
