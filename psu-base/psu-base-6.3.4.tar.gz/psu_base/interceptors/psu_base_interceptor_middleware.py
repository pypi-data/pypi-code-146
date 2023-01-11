from psu_base.classes.Log import Log
from psu_base.services import utility_service, message_service, error_service, downtime_service
from psu_base.services import auth_service
from psu_base.classes.Finti import Finti
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core import exceptions
from django.http import Http404
from django.http.multipartparser import MultiPartParserError
import re

log = Log()


class PsuBaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

        # Public views are defined in settings.py for each app: <APP_CODE>_PUBLIC_URLS
        #
        # As new public views are added to psu_base, the PSU_PUBLIC_URLS setting would need to be updated for
        # every existing app.  To avoid that, public psu_base views will now be listed here instead:
        psu_public_urls = [
            ".*/accounts/login",
            ".*/psu/messages",
            ".*/psu/test",
            ".*/psu/versions",
            ".*/psu/validate/date",
            ".*/psu/format/*",
            ".*/psu/menu_options/*",
            ".*/psu/toggle/simulation",
            ".*/psu/session/extend",
            ".*/psu/session/expired",
            ".*/authentication_error",
        ]

        # Authentication will be required on all pages, unless defined as public in settings
        self.public_views = []
        for ss in dir(settings):
            if ss.endswith("PUBLIC_URLS") and ss != "PSU_PUBLIC_URLS":
                urls = tuple(re.compile(url) for url in getattr(settings, ss))
                if urls:
                    self.public_views += list(urls)
        # Add in the PSU_BASE public URLs
        urls = tuple(re.compile(url) for url in psu_public_urls)
        if urls:
            self.public_views += list(urls)

        log.debug(f"PUBLIC URLS: {str(self.public_views)}")

    def process_view(self, request, view_func, view_args, view_kwargs):
        # By default, all pages require authentication
        # This can be disabled by setting REQUIRE_LOGIN to False in app_settings.py
        # When disabled, authentication will still be required for most psu plugin-provided views

        # No checking required when user is already authenticated
        if request.user.is_authenticated:
            # If logged in with a service account or -high account, this can still be an issue
            if (
                "authentication_error" not in request.path
                and "logout" not in request.path
            ):
                try:
                    if not auth_service.get_user().is_valid():
                        return redirect("psu:authentication_error")
                except Exception as ee:
                    log.error(
                        f"Unable to handle non-matching authentication (Django vs PSU): {ee}"
                    )
            return None

        # If requirement disabled, only need to check /psu/ urls
        elif "/psu/" not in request.path and not settings.REQUIRE_LOGIN:
            return None

        # Now, either all pages require auth, or this is a /psu/ path which may require auth
        else:
            # Has this page been defined as public?
            is_public = False
            for url in self.public_views:
                if url.match(request.path):
                    is_public = True

            # If public, no auth required
            if is_public:
                return None
            # Otherwise, require auth
            else:
                log.info(f"Authentication required for path: {request.path}")
                return login_required(view_func, login_url="cas:login")(
                    request, *view_args, **view_kwargs
                )

    def __call__(self, request):
        # Check for downtime and Finti connectivity
        next_downtime = downtime = connected = None
        try:
            # Check for PSU Base downtime (not Banner downtime)
            # Banner downtime is determined by Finti being down, which results in downtime page
            next_downtime = downtime_service.get_next_psu_base_downtime()
            downtime = next_downtime and next_downtime.is_active()
            # Allow certain page/role combinations to be accessed during downtime
            if downtime and any(request.path.startswith(x) for x in downtime_service.url_exemptions()):
                downtime = False
        except Exception as ee:
            error_service.record(ee)

        # A working Finti connection is required for all psu_base-enabled apps
        try:
            sid = Finti(suppress_logging=True).get("wdt/v1/sso_proxy/status")
            connected = sid and sid in ['oprd', 'stage', 'devl', 'test']
            if connected:
                utility_service.set_session_var("psu-base_last_connection_check", sid)

                # verify prod/nonprod agreement
                if utility_service.is_production() and sid != "oprd":
                    connected = False
                    log.error(f"Production instance is connected to {sid} database")
                elif utility_service.is_non_production() and sid == "oprd":
                    # Allow local development to connect to prod, but make it obvious
                    if utility_service.is_development():
                        message_service.post_error("WARNING: Connected to production database!")
                    else:
                        connected = False
                        log.error(f"{utility_service.get_environment()} instance is connected to production database")
        except Exception as ee:
            error_service.record(ee)
            connected = False

        # If either a downtime or Finti outage (or misconfiguration) is detected
        if downtime or not connected:
            if not connected:
                utility_service.set_session_var("psu-base_last_connection_check", None)
            log.warning(f"Downtime Page - Downtime: {next_downtime}, Connected: {connected}")
            return render(
                request, "psu_base/errors/disconnected.html",
                {"is_development": utility_service.is_development()}
            )

        # Is this an AWS health check or flash messages?
        flash_messages = request.path == reverse("psu:messages")
        is_scheduler = (
            "scheduler/run" in request.path or "scheduler/aws/run" in request.path
        )
        is_extension = "session/extend" in request.path
        silence_logs = (
            utility_service.is_health_check() or flash_messages or is_scheduler or is_extension
        )

        # Before the view (and later middleware) are called.
        if not flash_messages:
            # Getting sub-app info now keeps APP_CODE consistent for entire request (when changing sub-apps)
            app_code = utility_service.get_app_code()
            sub_app_info = utility_service.get_sub_app_info()
        auth_service.set_sso_user(request)

        # In non-prod, make the start of a new request more visible in the log (console)
        if not silence_logs:
            auth_string = "Anonymous"
            auth = request.session.get("psu_base_auth_object")
            if auth:
                sso = auth.get("sso_user")
                imp = auth.get("impersonated_user")
                prx = auth.get("proxied_user")
                if sso:
                    auth_string = sso.get("username")
                    if imp and imp.get("username"):
                        auth_string += f"/{imp.get('username')}"
                    if prx and prx.get("username"):
                        auth_string += f" proxying {prx.get('username')}"
            w = 80
            log.debug(
                f"\n{'='.ljust(w, '=')}\n{f'Request:  {auth_string}  {request.path}'}\n{'='.ljust(w, '=')}"
            )
            log.trace([request.path], "Request")
        elif flash_messages:
            log.debug("=== Flash Messages ===")
        elif is_extension:
            log.debug("=== Session Extended ===")

        # Remove flash variables from two requests ago. Shift flash variables from last request.
        # This happens for every request EXCEPT posting flash messages to the screen
        if (not flash_messages) and (not is_extension):
            utility_service.cycle_flash_scope()

            # If a delayed flash message was saved, post it now
            for kk in request.session.keys():
                if kk.startswith("flashed_scope_delayed_message:"):
                    level = kk.split(":")[1]
                    msg = request.session.get(kk)
                    message_service.post_message(msg, level)

        # Render the response
        response = self.get_response(request)

        # After the view has completed
        utility_service.clear_page_scope()

        if not silence_logs:
            log.end(request.path, "Request")

        return response
    
    def process_exception(self, request, exception):
        http_4xx_exceptions = (
            Http404,
            exceptions.PermissionDenied,
            MultiPartParserError,
            exceptions.BadRequest,
            exceptions.SuspiciousOperation,
        )
        
        if not isinstance(exception, http_4xx_exceptions):
            error_service.unexpected_error(error_system=exception, debug_info="Error 500 - Unhandled Exception")
