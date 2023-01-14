from typing import Optional

from pydantic import BaseModel


class Proxy(BaseModel):
    host: str
    port: str
    user: Optional[str]
    password: Optional[str]

    def __str__(self):
        """Convert a proxy object to a string in the format of "ip:port" or
        "ip:port:user:pass".
        """

        if self.user and self.password:
            return f"{self.host}:{self.port}:{self.user}:{self.password}"
        else:
            return f"{self.host}:{self.port}"

    def to_dict(self):
        """Convert a proxy object to a dict which can be passed to the
        requests module.

        {
            'http': 'http://host:post@user:password',
            'https': 'http://host:post@user:password'
        }
        """

        if not self.host and not self.port:
            return {}

        proxy_url = f"{self.host}:{self.port}"
        if self.user and self.password:
            proxy_url = f"{self.user}:{self.password}@{proxy_url}"

        return {
            "http": f"http://{proxy_url}",
            "https": f"http://{proxy_url}",
        }

    @staticmethod
    def from_string(string: str):
        """Convert a proxy formatted as string ("ip:port" or
        "ip:port:user:pass") to a proxy object.

        :param string: "ip:port" or "ip:port:user:pass"
        :return: proxy object
        """

        host, port, *authentication = string.split(":", 4)
        if authentication:
            user, password = authentication
        else:
            user = None
            password = None

        return Proxy(host=host, port=port, user=user, password=password)

    @staticmethod
    def from_json(o: dict):
        return Proxy(**o)

    @classmethod
    def many_from_json(cls, objs):
        return [cls.from_json(o) for o in objs]
