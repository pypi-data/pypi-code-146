##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from ._version import __version__

import json, time, os, base64, re, hashlib, random, requests, webbrowser
from urllib import request, parse
import tornado.httpserver
import tornado.ioloop
import tornado.web

from optumi_core.logging import optumi_format_and_log

DEBUG = False
dev_version = "dev" in __version__.lower()

# This is OKTA stuff
LOGIN_SERVER = "https://olh.optumi.net:8443"
REDIRECT_URI = LOGIN_SERVER + "/redirect"
BASE_URL = "https://login.optumi.com"
AUTH_SERVER_ID = "default"
CLIENT_ID = "0oa1seifygaiUCgoA5d7"

LOGIN_WRAP_START = '<div style="position: absolute;top: 40%;width: calc(100% - 16px);"><div style="display: grid;justify-content: center;"><img style="margin: auto;" src="https://www.optumi.com/wp-content/uploads/2020/10/optumi-logo-header.png" srcset="https://www.optumi.com/wp-content/uploads/2020/10/optumi-logo-header.png 1x" width="200" height="50" alt="Optumi Logo" retina_logo_url="" class="fusion-standard-logo"><div style="text-align: center;font-size: 1.5rem">'
LOGIN_WRAP_END = "</div></div></div>"

login_state = None
login_pkce = None
login_token = None


def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    return {"code_verifier": code_verifier, "code_challenge": code_challenge}


def generate_state():
    randomCharset = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ret = ""
    for i in range(64):
        ret += randomCharset[random.randint(0, len(randomCharset) - 1)]
    return ret


last_login_time = None


class OauthLoginHandler(tornado.web.RequestHandler):
    async def get(self):
        global login_state
        global login_pkce
        global last_login_time

        now = time.time()
        if last_login_time != None and now - last_login_time < 0.5:
            raise Exception("Blocking rapid logins")
        last_login_time = now

        if dev_version:
            print(optumi_format_and_log(self, "OAUTH login initiated"))
        else:
            optumi_format_and_log(self, "OAUTH login initiated")

        try:
            login_pkce = generate_pkce()
            login_state = {
                "state": generate_state(),
                "origin": self.request.protocol + "://" + self.request.host,
            }

            data = {
                "client_id": CLIENT_ID,
                "response_type": "code",
                "scope": "openid",
                "redirect_uri": REDIRECT_URI,
                "state": json.dumps(login_state),
                "code_challenge_method": "S256",
                "code_challenge": login_pkce["code_challenge"],
            }
            url_data = parse.urlencode(data)
            url = BASE_URL + "/oauth2/" + AUTH_SERVER_ID + "/v1/authorize?" + url_data

            self.redirect(url)
        except Exception as e:
            self.set_status(401)
            self.write(json.dumps({"message": "Encountered error setting login state"}))
            print(optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


class OauthCallbackHandler(tornado.web.RequestHandler):
    async def get(self):
        global login_state
        global login_pkce
        global login_token
        global loginProgress
        try:
            code = self.get_argument("code")
            state = json.loads(self.get_argument("state"))

            if json.dumps(login_state, sort_keys=True) != json.dumps(
                state, sort_keys=True
            ):
                raise Exception("State does not match expected state in oauth callback")

            ## Exchange code for access and id token

            url = "https://dev-68278524.okta.com/oauth2/" + AUTH_SERVER_ID + "/v1/token"

            payload = {
                "client_id": CLIENT_ID,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
                "code": code,
                "code_verifier": login_pkce["code_verifier"],
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            # Reset these so they can't be used again
            login_state = None
            login_pkce = None

            login_token = response.text

            loginProgress = "Allocating..."

            self.write(
                LOGIN_WRAP_START
                + "You have successfully logged into Optumi and you can close this tab"
                + LOGIN_WRAP_END
            )

            # If we want to access parts of the token here, we can do so like this:
            # token = json.loads(login_token)
            # print(token['access_token'])
            # print(token['id_token'])

            tornado.ioloop.IOLoop.current().stop()
        except Exception as e:
            self.set_status(401)
            self.write(
                json.dumps(
                    {"message": "Encountered error while handling oauth callback"}
                )
            )
            print(optumi_format_and_log(self, str(e)))
            if DEBUG:
                raise e


def make_app():
    app = tornado.web.Application(
        [
            (r"/optumi/oauth-callback", OauthCallbackHandler),
            (r"/optumi/oauth-login", OauthLoginHandler),
        ]
    )
    sockets = tornado.netutil.bind_sockets(0, "")
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    return "http://localhost:%d/optumi/oauth-login" % sockets[0].getsockname()[1]


def login():
    # Open URL in a new tab, if a browser window is already open.
    webbrowser.open_new_tab(make_app())
    tornado.ioloop.IOLoop.current().start()
    return login_token


if __name__ == "__main__":
    print(login())
