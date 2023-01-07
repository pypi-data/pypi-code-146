import logging
from urllib.parse import urlparse, urlunparse
from time import sleep

from requests import Session
import requests

from .csrf import ParseCSRF


class Hostea:
    def __init__(self, username: str, email: str, password: str, host: str, c: Session):
        self.username = username
        self.email = email
        self.password = password
        self.csrf_key = "csrfmiddlewaretoken"
        self.host = host
        self.c = c

    @staticmethod
    def check_online(dashboard_host: str, maildev_host: str):
        """
        Check if Hostea Dashboard is online
        """
        count = 0
        dash_parsed = urlparse(dashboard_host)
        maildev_parsed = urlparse(maildev_host)
        urls = [
            urlunparse((dash_parsed.scheme, dash_parsed.netloc, "/login/", "", "", "")),
            urlunparse((maildev_parsed.scheme, maildev_parsed.netloc, "", "", "", "")),
        ]

        for url in urls:
            while True:
                try:
                    res = requests.get(url, allow_redirects=False)
                    if any([res.status_code == 302, res.status_code == 200]):
                        break
                except Exception as e:
                    sleep(2)
                    print(e)
                    print(f"[Hostea] Retrying {count} time for {url}")
                    count += 1
                    continue

    def get_uri(self, path: str):
        parsed = urlparse(self.host)
        return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))

    def get_csrf(self, url: str) -> str:
        resp = self.c.get(url=url)
        assert resp.status_code == 200
        parser = ParseCSRF(name=self.csrf_key)
        parser.feed(resp.text)
        csrf = parser.token
        assert csrf != ''
        return csrf

    def __get_verification_link(self, maildev_host: str):
        def maildev_uri(maildev_host: str, path: str):
            parsed = urlparse(maildev_host)
            return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))

        resp = self.c.get(maildev_uri(maildev_host=maildev_host, path="/email/"))
        #        resp = self.c.get("http://localhost:1080/email/")
        emails = resp.json()
        for email in emails:
            if email["to"][0]["address"] == self.email:
                logging.info("[Dashboard] Found verification link")
                resp = self.c.delete(
                    maildev_uri(maildev_host=maildev_host, path=f"/email/{email['id']}")
                )
                return str.strip(email["text"].split("\n")[1])
        logging.critical("[Dashboard] Verification link not found")

    def register(self, maildev_host: str):
        url = self.get_uri("/register/")
        csrf = self.get_csrf(url)
        payload = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "confirm_password": self.password,
            self.csrf_key: csrf,
        }

        logging.info("Registering user")
        resp = self.c.post(url, payload, allow_redirects=False)
        assert resp.status_code == 302
        assert "pending" in resp.headers["Location"]

        email_verification_link = self.__get_verification_link(
            maildev_host=maildev_host
        )
        csrf = self.get_csrf(email_verification_link)
        payload = {
            self.csrf_key: csrf,
        }
        resp = self.c.post(email_verification_link, payload, allow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["Location"] == "/login/"
        logging.info("[Dashboard] Email verified user")

    def login(self):
        url = self.get_uri("/login/")

        csrf = self.get_csrf(url)
        payload = {
            "login": self.username,
            "password": self.password,
            self.csrf_key: csrf,
        }
        print(f"payload {payload}")
        logging.info("Logging In user")
        resp = self.c.post(url, data=payload, allow_redirects=False)

        assert resp.status_code == 302, resp.text
        assert resp.headers["Location"] == "/"

        resp = self.c.get(self.get_uri("/support/new/"))
        assert resp.status_code == 200

#    def new_ticket(self, support_repository_new_issue: str):
#        resp = self.c.get(self.get_uri("/support/new/"))


#        print(resp.text)
#        print(support_repository_new_issue)
#        assert support_repository_new_issue in resp.text
