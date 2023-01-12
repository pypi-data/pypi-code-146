import logging
import webbrowser

import requests

from gdshoplib.core.settings import VKSettings

logger = logging.getLogger(__name__)


class VKNotFoundException(Exception):
    ...


class VK:
    def __init__(self):
        self.settings = VKSettings()

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.settings.VK_USER_ACCESS_TOKEN}"}

    def request(self, method, params=None):
        _params = {"v": self.settings.VK_API_VERSION}
        _params.update(params or {})

        r = requests.get(
            f"{self.settings.VK_BASEPATH}{method}",
            params=_params,
            headers=self.auth_headers(),
        )

        if not r.ok:
            logger.warning(r.json())
            if r.status_code == 404:
                raise VKNotFoundException

            assert False, f"Запрос {method} {params} прошел с ошибкой {r.status_code}/n"

        return r.json()

    def get_oauth_code(self):
        # Получить токен для работы
        # Принять код, получить access_token и напечатать его
        webbrowser.open(self.get_user_code_url())

    def get_access_token(self, code):
        r = requests.get(self.get_user_access_token_url(code))
        assert r.ok, "Запрос прошел с ошибкой"

        print(r.json())

    def get_user_code_url(self):
        return self.create_url(
            "https://oauth.vk.com/authorize",
            dict(
                client_id=self.settings.VK_CLIENT_ID,
                display="page",
                scope=self.settings.VK_USER_SCOPE,
                response_type="code",
                v=self.settings.VK_API_VERSION,
            ),
        )

    def get_user_access_token_url(self, code):
        assert self.settings.VK_SECRET_KEY, "VK_SECRET_KEY не определен"
        return self.create_url(
            "https://oauth.vk.com/access_token",
            dict(
                client_id=self.settings.VK_CLIENT_ID,
                client_secret=self.settings.VK_SECRET_KEY,
                code=code,
            ),
        )

    @staticmethod
    def create_url(base_path, params):
        path = f"{base_path}?"
        for k, v in params.items():
            path += f"{k}={v}&"

        return path[:-1]
