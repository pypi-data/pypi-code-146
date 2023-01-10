#!/opt/venvs/securedrop-app-code/bin/python
# -*- coding: utf-8 -*-

import os
import sys

os.environ["SECUREDROP_ENV"] = "dev"  # noqa
import journalist_app

from sdconfig import config
from db import db
from models import Journalist


def main(username, password, otp_secret):
    app = journalist_app.create_app(config)
    with app.app_context():

        user = Journalist(username=username,
                          password=password,
                          is_admin=True,
                          first_name="",
                          last_name="")
        user.otp_secret = otp_secret
        db.session.add(user)
        db.session.commit()


main(*sys.argv[1:])
