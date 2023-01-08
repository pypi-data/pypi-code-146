import hashlib
import uuid
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

from .defaults import (
    PASSWORDLESS_HASH_SALT,
    PASSWORDLESS_OTP_DICTIONARY,
    PASSWORDLESS_OTP_LENGTH,
    PASSWORDLESS_USE_CELERY,
)
from .tasks import celery_send_email


class AuthRequest(models.Model):
    REQUEST_TYPE_CHOICES = (
        ("E", "Change Email"),
        ("L", "Login"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, editable=False)
    type = models.CharField(max_length=1, choices=REQUEST_TYPE_CHOICES, editable=False)
    hash = models.CharField(
        max_length=64,
        db_index=True,
        blank=True,
        null=True,
        editable=False,
    )
    otp = models.CharField(max_length=24, blank=True, null=True, editable=False)
    email_sent = models.BooleanField(default=False, editable=False)
    is_used = models.BooleanField(default=False, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Passwordless request"

    def create_otp(self):
        otp_length = getattr(
            settings,
            "PASSWORDLESS_OTP_LENGTH",
            PASSWORDLESS_OTP_LENGTH,
        )
        dictionary = getattr(
            settings,
            "PASSWORDLESS_OTP_DICTIONARY",
            PASSWORDLESS_OTP_DICTIONARY,
        )

        otp = []
        while len(otp) < otp_length:
            otp.append(dictionary[randint(0, len(dictionary) - 1)])

        return "".join(otp)

    def create_hash(self):
        salt = getattr(
            settings,
            "PASSWORDLESS_HASH_SALT",
            PASSWORDLESS_HASH_SALT,
        )

        plaintxt = ":".join(["djangopasswordless", self.email, salt])
        return hashlib.sha256(plaintxt.encode()).hexdigest()

    def public_hash(self):
        return f"{self.hash}{self.id}".replace("-", "").lower()

    def send_otp(self):
        context = {
            "email": self.email,
            "hash": self.public_hash(),
            "otp": self.otp,
        }

        # select appropriate templates
        if self.type == "L":
            subject = "passwordless/email/login_subject.txt"
            msghtml = "passwordless/email/login_message.html"
            msgtxt = "passwordless/email/login_message.txt"
        else:
            subject = "passwordless/email/changeemail_subject.txt"
            msghtml = "passwordless/email/changeemail_message.html"
            msgtxt = "passwordless/email/changeemail_message.txt"

        # send email
        send_mail(
            render_to_string(subject, context=context),
            render_to_string(msgtxt, context=context),
            None,
            [self.email],
            html_message=render_to_string(msghtml, context=context),
            fail_silently=False,
        )

        self.email_sent = True
        self.save()

    def save(self, *args, **kwargs):
        if self.otp is None:
            self.otp = self.create_otp()

        if self.hash is None:
            self.hash = self.create_hash()

        super(AuthRequest, self).save(*args, **kwargs)

        if not self.email_sent:
            use_celery = getattr(
                settings,
                "PASSWORDLESS_USE_CELERY",
                PASSWORDLESS_USE_CELERY,
            )

            if use_celery:
                celery_send_email.delay(self.id)
            else:
                self.send_otp()


class AuthFailure(models.Model):
    hash = models.CharField(max_length=64, db_index=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ("-created",)
        verbose_name = "Passwordless failure"
