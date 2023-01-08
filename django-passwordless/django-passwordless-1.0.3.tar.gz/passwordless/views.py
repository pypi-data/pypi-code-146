import uuid
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.views.generic import TemplateView

from .defaults import (
    PASSWORDLESS_MAX_REQUEST_AGE,
    PASSWORDLESS_MAX_REQUEST_COUNT,
    PASSWORDLESS_MAX_REQUEST_FAILURES,
    PASSWORDLESS_REGISTRATION_ENABLED,
)
from .forms import PasswordlessRequestForm, PasswordlessOTPForm
from .models import AuthFailure, AuthRequest


class PasswordlessBaseView(TemplateView):
    def get_cutoff(self):
        return now() - timedelta(
            seconds=getattr(
                settings,
                "PASSWORDLESS_MAX_REQUEST_AGE",
                PASSWORDLESS_MAX_REQUEST_AGE,
            )
        )

    def get_request(self, hash, type):
        return (
            AuthRequest.objects.filter(hash=hash)
            .filter(type=type)
            .order_by("-created")
            .first()
        )

    def get_request_by_otp(self, hash, type, otp):
        return (
            AuthRequest.objects.filter(hash=hash)
            .filter(is_used=False)
            .filter(created__gte=self.get_cutoff())
            .filter(type=type)
            .filter(otp__iexact=otp)
            .first()
        )

    def get_user(self, email):
        return get_user_model().objects.filter(email=email).first()

    def max_failures(self):
        return getattr(
            settings,
            "PASSWORDLESS_MAX_REQUEST_FAILURES",
            PASSWORDLESS_MAX_REQUEST_FAILURES,
        )

    def max_requests(self):
        return getattr(
            settings,
            "PASSWORDLESS_MAX_REQUEST_COUNT",
            PASSWORDLESS_MAX_REQUEST_COUNT,
        )

    def registration_enabled(self):
        return getattr(
            settings,
            "PASSWORDLESS_REGISTRATION_ENABLED",
            PASSWORDLESS_REGISTRATION_ENABLED,
        )

    def valid_request_exists(self, hash, id, type):
        return (
            AuthRequest.objects.filter(hash=hash)
            .filter(id=id)
            .filter(is_used=False)
            .filter(created__gte=self.get_cutoff())
            .filter(type=type)
            .exists()
        )


class PasswordlessChangeEmailRequestView(LoginRequiredMixin, PasswordlessBaseView):
    template_name = "passwordless/changeemail_request.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["form"] = PasswordlessRequestForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        fail_reason = None
        context = self.get_context_data(**kwargs)

        form = PasswordlessRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()

            # reject if an account already exists with this email address
            if self.get_user(email) is not None:
                fail_reason = "account_exists"

            # the request is valid, create the auth_request object
            if not fail_reason:
                ar = AuthRequest(email=email, type="E", user=request.user)
                ar.save()

                # redirect to the otp form
                path = request.path
                if not request.path.endswith("/"):
                    path = f"{request.path}/"
                return redirect(f"{path}{ar.public_hash()}")

        context["form"] = form
        context["fail_reason"] = fail_reason
        return self.render_to_response(context)


class PasswordlessChangeEmailOTPView(LoginRequiredMixin, PasswordlessBaseView):
    template_name = "passwordless/changeemail_otp.html"

    def get(self, request, *args, **kwargs):
        return self.respond(request, kwargs["key"])

    def post(self, request, *args, **kwargs):
        return self.respond(request, kwargs["key"])

    def respond(self, request, key):
        hash = key[0:64]
        id = key[64:]
        context = self.get_context_data()

        # show an error if no valid request exists
        if not self.valid_request_exists(hash, id, "E"):
            self.template_name = "passwordless/changeemail_otp_unknown.html"
            return self.render_to_response(context)

        if request.method == "POST":
            form = PasswordlessOTPForm(request.POST)
            if form.is_valid():
                ar = self.get_request_by_otp(hash, "E", form.cleaned_data["otp"])
                if ar is None:
                    AuthFailure(hash=hash).save()
                    context["bad_otp"] = True
                else:
                    # mark the request as used
                    ar.is_used = True
                    ar.save()

                    # update the user's email address
                    previous_email = ar.user.email
                    ar.user.email = ar.email
                    ar.user.save()

                    # add message
                    message = render_to_string(
                        "passwordless/messages/changeemail_success.html",
                        context={
                            "previous_email": previous_email,
                            "new_email": ar.email,
                        },
                    )
                    if len(message) > 0:
                        messages.add_message(request, messages.SUCCESS, message)

                    # login and redirect
                    return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))

            context["form"] = form
        else:
            context["form"] = PasswordlessOTPForm()

        context["email"] = self.get_request(hash, "E").email
        return self.render_to_response(context)


class PasswordlessLoginRequestView(PasswordlessBaseView):
    template_name = "passwordless/login_request.html"

    def get(self, request, *args, **kwargs):
        # redirect away if already authenticated
        if request.user.is_authenticated:
            return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))

        context = self.get_context_data(**kwargs)
        context["form"] = PasswordlessRequestForm()
        context["registration_enabled"] = self.registration_enabled()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # redirect away if already authenticated
        if request.user.is_authenticated:
            return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))

        fail_reason = None
        context = self.get_context_data(**kwargs)

        form = PasswordlessRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()

            # if too many requests, show an error
            if self.request_count_exceeded(email):
                fail_reason = "request_count_exceeded"

            # if registration is disabled, and we don't know this user, show an error
            if (
                not fail_reason
                and not self.registration_enabled()
                and not self.get_user(email)
            ):
                fail_reason = "registration_disabled"

            # the request is valid, create the auth_request object
            if not fail_reason:
                ar = AuthRequest(email=email, type="L")
                ar.save()

                # redirect to the otp form
                path = request.path
                if not request.path.endswith("/"):
                    path = f"{request.path}/"
                return redirect(f"{path}{ar.public_hash()}")

        context["form"] = form
        context["fail_reason"] = fail_reason
        context["registration_enabled"] = self.registration_enabled()
        return self.render_to_response(context)

    def request_count_exceeded(self, email):
        return (
            AuthRequest.objects.filter(email=email)
            .filter(is_used=False)
            .filter(created__gte=self.get_cutoff())
            .count()
        ) >= self.max_requests()


class PasswordlessLoginOTPView(PasswordlessBaseView):
    template_name = "passwordless/login_otp.html"

    def get(self, request, *args, **kwargs):
        return self.respond(request, kwargs["key"])

    def post(self, request, *args, **kwargs):
        return self.respond(request, kwargs["key"])

    def respond(self, request, key):
        # redirect away if already authenticated
        if request.user.is_authenticated:
            return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))

        hash = key[0:64]
        id = key[64:]
        context = self.get_context_data()

        # show an error if no valid request exists
        if not self.valid_request_exists(hash, id, "L"):
            self.template_name = "passwordless/login_otp_unknown.html"
            return self.render_to_response(context)

        # show an error if the rate limit has been reached
        if self.failure_limit_reached(hash):
            self.template_name = "passwordless/login_otp_ratelimit.html"
            return self.render_to_response(context)

        if request.method == "POST":
            form = PasswordlessOTPForm(request.POST)
            if form.is_valid():
                # Find unused request of the same hash. Note, it does not have to have
                # the matching ID, for the scenario where the user has multiple emails
                # and is looking at the wrong otp. Keep it friendly for the user.
                # Security is not comprimised as they must have followed a valid link to
                # get this far.
                ar = self.get_request_by_otp(hash, "L", form.cleaned_data["otp"])
                if ar is None:
                    AuthFailure(hash=hash).save()
                    context["bad_otp"] = True
                else:
                    # mark the request as used
                    ar.is_used = True
                    ar.save()

                    # fetch the user, create if they don't exist
                    user = self.get_user(email=ar.email)
                    if user:
                        message = render_to_string(
                            "passwordless/messages/login_success.html",
                            context={"email": ar.email},
                        )
                    else:
                        user = get_user_model().objects.create_user(
                            str(uuid.uuid4()),
                            email=ar.email,
                        )
                        message = render_to_string(
                            "passwordless/messages/createuser_success.html",
                            context={"email": ar.email},
                        )

                    # add message
                    if len(message) > 0:
                        messages.add_message(request, messages.SUCCESS, message)

                    # login and redirect
                    login(request, user)
                    return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))

            context["form"] = form
        else:
            context["form"] = PasswordlessOTPForm()

        context["email"] = self.get_request(hash, "L").email
        return self.render_to_response(context)

    def failure_limit_reached(self, hash):
        return (
            AuthFailure.objects.filter(hash=hash)
            .filter(created__gte=self.get_cutoff())
            .count()
            >= self.max_failures()
        )
