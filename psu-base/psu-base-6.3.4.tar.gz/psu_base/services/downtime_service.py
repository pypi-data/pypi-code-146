import pytz
from psu_base.models.downtime import Downtime
from psu_base.classes.BannerDowntime import BannerDowntime
from psu_base.classes.Log import Log
from datetime import datetime, timedelta
from psu_base.services import utility_service, error_service, auth_service
import urllib
import json

log = Log()

warning_minutes = 30
downtime_path = utility_service.get_static_content_url() + "/downtime/downtime.json"


def url_exemptions():
    """
    Allow certain paths to be used during downtimes
    """
    # Allow anyone (with required authorities, of course)
    anyone = [
        "/psu/messages",  # Flash messages
        "/psu/test",      # Status page (also AWS health check in most apps)
        "/psu/xss",       # XSS blocking page
    ]

    # Only for admins (with any additional required authorities)
    admins = [
        "/psu/downtime/list",   # Downtime list
        "/psu/errors",          # Error log
        "/psu/error_status",    # Error log
        "/psu/emails",          # Email log
        "/psu/audit",           # Audit logs
    ]

    # Only for developers
    devs = [
        "/psu/features",         # Feature Toggles
        "/psu/modify_feature",   # Update feature toggle
        "/psu/export",           # AWS data export/download (menu)
        "/psu/session",          # Examine session
        "/psu/variables",        # Site variable management
        "/psu/modify_variable",  # Site variable management
        "/psu/delete_variable",  # Site variable management
        "/psu/fixture_export",   # AWS data export/download (action)
        "/psu/downtime/add",     # Downtime management
        "/psu/downtime/delete",  # Downtime management
        "/psu/downtime/end",     # Downtime management
    ]
    if auth_service.has_authority("developer"):
        return anyone + admins + devs
    elif auth_service.has_authority("~PowerUser"):
        return anyone + admins
    else:
        return anyone


def get_next_downtime():
    next_dt = None
    try:
        downtimes = []
        base = get_next_psu_base_downtime()
        if base:
            downtimes.append(base)

        banner = get_next_banner_downtime()
        if banner:
            # Ignore Banner downtimes > X minutes from now
            now = datetime.now()
            cutoff = now + timedelta(minutes=warning_minutes)
            if banner.from_date < cutoff:
                downtimes.append(banner)

        if downtimes:
            next_dt = sorted(downtimes, key=lambda x: x.minutes_until_start())[0]

        if next_dt and next_dt.is_active():
            return next_dt

        elif banner is False:
            # Indicates a Finti connection error
            return False

        else:
            return next_dt

    except Exception as ee:
        error_service.record(ee)
        return False


def get_next_psu_base_downtime():
    """Get the next (includes current active) downtime"""
    try:
        now = datetime.now()
        cutoff = now + timedelta(minutes=warning_minutes)

        if utility_service.get_setting('USE_TZ') and not now.tzinfo:
            america_vancouver = pytz.timezone('America/Vancouver')
            now = america_vancouver.localize(now)
            cutoff = america_vancouver.localize(cutoff)

        downtimes = (
            Downtime.objects.filter(from_date__lte=cutoff)
            .exclude(until_date__lte=now)
            .order_by("from_date")
        )
        if downtimes:
            return downtimes[0]
    except Exception as ee:
        error_service.record(ee)

    return None


def get_banner_downtime_json_content():
    # Do not need to get this multiple times per request
    # However, a downtime can prevent the page/flash scopes from cycling (feature, not a bug)
    # JSON could get updated during downtime
    # Use persistent session, but refresh every X minutes
    now = int(datetime.now().strftime("%H%M"))
    last_save = utility_service.get_page_scope("psu_base-downtime-json_timestamp")

    # Always read when no content exists yet
    read_from_file = last_save is None

    # Re-read if more than 3 minutes has passed
    if not read_from_file:
        then = int(last_save)
        if now < then:
            # next day
            read_from_file = True

        elif now - then > 3:
            read_from_file = True

    if read_from_file:
        # Save the timestamp
        utility_service.set_page_scope("psu_base-downtime-json_timestamp", now)

        # Get JSON string from static-content server
        file_contents = urllib.request.urlopen(downtime_path).read().decode()

        # For local development, allow reading from a local file in the root directory
        if utility_service.is_development():
            log.debug("IS DEV *******************************")
            import os
            dev_json_file = os.path.join(os.getcwd(), "downtime.json")
            if os.path.isfile(dev_json_file):
                log.debug("READING FROM LOCAL FILE *******************************")
                with open(dev_json_file) as f:
                    file_contents = f.read()
                    log.debug(f"\n\n{file_contents}\n\n***************************************")

        return utility_service.set_page_scope("psu_base-downtime-json_content", file_contents)
    else:
        return utility_service.get_page_scope("psu_base-downtime-json_content")


def get_banner_downtimes():
    """
    Returns:
        A list of BannerDowntime objects (past, present, and future)
        - Sorted latest (likely in the future) to oldest (in the past)
    """
    downtime_list = []
    try:
        # Get downtimes from <static-content>/downtime/downtime.json
        downtime_json = get_banner_downtime_json_content()
        try:
            downtimes = json.loads(downtime_json)
        except Exception as ee:
            error_service.record(ee, downtime_json)
            downtimes = None

        if downtimes and type(downtimes) is list:
            is_prod = utility_service.is_production()
            for dt in downtimes:
                this_dt = BannerDowntime(dt)
                # Non-prod downtimes are ignored in prod
                # (prod downtimes are included in any environment)
                if is_prod and not this_dt.is_prod_downtime():
                    continue
                # Add this downtime to the list of downtime objects
                downtime_list.append(this_dt)

            # Sort downtimes by start date
            downtime_list = sorted(downtime_list, key=lambda x: x.minutes_until_start(), reverse=True)
    except Exception as ee:
        error_service.record(ee)
    return downtime_list


def get_next_banner_downtime():
    """
    Returns:
        1. A BannerDowntime object for the next (or current) downtime
        2. None (No active/future downtimes exist)
    """
    next_dt = None
    try:
        eligible_dts = []
        for dt in get_banner_downtimes():
            # Ignore FYE downtimes, which are only used by Cashnet features
            if dt.reason and dt.reason.upper() == "FYE":
                log.debug(f"SKIP FYE: {dt}")
                continue
            if not dt.is_past():
                eligible_dts.append(dt)
        if eligible_dts:
            eligible_dts = sorted(eligible_dts, key=lambda x: x.minutes_until_start())
            next_dt = eligible_dts[0]
    except Exception as ee:
        error_service.record(ee)
    return next_dt


def get_next_fye_downtime():
    """
    This would likely only be used by the Cashnet plugin

    Returns:
        1. A BannerDowntime object for the next (or current) Fiscal Year End downtime
        2. None (No active/future downtimes exist)
    """
    next_dt = None
    try:
        eligible_dts = []
        for dt in get_banner_downtimes():
            # Ignore non-FYE downtimes
            if not dt.reason:
                continue
            if dt.reason.upper() != "FYE":
                continue
            if not dt.is_past():
                eligible_dts.append(dt)
        if eligible_dts:
            eligible_dts = sorted(eligible_dts, key=lambda x: x.minutes_until_start())
            next_dt = eligible_dts[0]
    except Exception as ee:
        error_service.record(ee)
    return next_dt
