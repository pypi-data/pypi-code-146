# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import current_app
from flask import render_template

from .tasks import start_send_mail_task


def send_email_confirmation_mail(email, displayname, token, expires_in):
    """Send an email confirmation mail in a background task.

    Uses :func:`kadi.modules.notifications.tasks.start_send_mail_task` to send the mail.

    :param email: The recipient address.
    :param displayname: The display name of the addressed user.
    :param token: A JSON web token as returned by
        :meth:`.LocalIdentity.get_email_confirmation_token` corresponding to the
        identity of the addressed user.
    :param expires_in: The time in seconds the token will expire in.
    :return: ``True`` if the task was started successfully, ``False`` otherwise.
    """
    kwargs = {"displayname": displayname, "token": token, "expires_in": expires_in}

    text_message = render_template(
        "notifications/mails/email_confirmation.txt", **kwargs
    )
    html_message = render_template(
        "notifications/mails/email_confirmation.html", **kwargs
    )

    return start_send_mail_task(
        subject=f"[{current_app.config['MAIL_SUBJECT_HEADER']}] Email confirmation",
        message=text_message,
        html_message=html_message,
        to_addresses=[email],
    )


def send_password_reset_mail(email, displayname, token, expires_in):
    """Send a password reset mail in a background task.

    Uses :func:`kadi.modules.notifications.tasks.start_send_mail_task` to send the mail.

    :param email: The recipient address.
    :param displayname: The display name of the addressed user.
    :param token: A JSON web token as returned by
        :meth:`.LocalIdentity.get_password_reset_token` corresponding to the identity of
        the addressed user.
    :param expires_in: The time in seconds the token will expire in.
    :return: ``True`` if the task was started successfully, ``False`` otherwise.
    """
    kwargs = {"displayname": displayname, "token": token, "expires_in": expires_in}

    text_message = render_template("notifications/mails/password_reset.txt", **kwargs)
    html_message = render_template("notifications/mails/password_reset.html", **kwargs)

    return start_send_mail_task(
        subject=f"[{current_app.config['MAIL_SUBJECT_HEADER']}] Password reset request",
        message=text_message,
        html_message=html_message,
        to_addresses=[email],
    )


def send_test_mail(email, displayname):
    """Send a test mail in a background task.

    Uses :func:`kadi.modules.notifications.tasks.start_send_mail_task` to send the mail.

    :param email: The recipient address.
    :param displayname: The display name of the addressed user.
    :return: ``True`` if the task was started successfully, ``False`` otherwise.
    """
    text_message = render_template(
        "notifications/mails/test_email.txt", displayname=displayname
    )
    html_message = render_template(
        "notifications/mails/test_email.html", displayname=displayname
    )

    return start_send_mail_task(
        subject=f"[{current_app.config['MAIL_SUBJECT_HEADER']}] Test email",
        message=text_message,
        html_message=html_message,
        to_addresses=[email],
    )
