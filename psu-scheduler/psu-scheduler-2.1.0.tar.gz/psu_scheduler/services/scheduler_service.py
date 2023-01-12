from collections import OrderedDict
from datetime import datetime, timedelta
from psu_base.classes.Log import Log
from psu_base.context_processors import util as util_context
from psu_base.services import utility_service, error_service
from psu_base.classes.Finti import Finti
from psu_scheduler.models import ScheduledJob, JobExecution, EndpointDefinition

log = Log()


def get_app_codes():
    """
    Since jobs are called from the base app, but may be defined/scheduled from a sub app, all
    queries must accept any app_code in the current project
    """
    if utility_service.sub_apps():
        app_codes = list(utility_service.sub_apps().keys())
        app_codes.append(utility_service.get_app_code())
    else:
        app_codes = [utility_service.get_app_code()]

    return app_codes


def call_jobs_via_finti():
    """
    Run scheduled jobs via Finti
    This was created to run scheduled jobs via AWS Health Check, which was not able to call them directly
    """
    # When called from AWS Health Check, the URL from get_absolute_url() is an IP address
    # Rather, use the HOST_URL setting
    host_url = conventional_url = utility_service.get_setting('HOST_URL')

    # Or, use a convention-based URL if HOST_URL is not set
    if not host_url:
        app = utility_service.get_app_code().lower().replace('_', '-')
        env = utility_service.get_environment().lower()  # dev, stage, prod
        conventional_url = f"https://{app}{f'-{env}' if env != 'prod' else ''}.campus.wdt.pdx.edu"

    # Allow a specific SCHEDULER_URL setting to override conventional URL
    override_url = utility_service.get_setting("SCHEDULER_URL")

    address = override_url or host_url
    if not address:
        address = conventional_url

    return Finti().get("wdt/v1/sso_proxy/scheduled_jobs", {'address': address})


def get_jobs_to_run():
    """
    Check each defined job to see if it needs to run
    """
    log.trace()
    jobs = ScheduledJob.objects.filter(app_code__in=get_app_codes())
    run_list = []
    if jobs:
        for jj in jobs:
            if jj.should_run():
                run_list.append(jj)
    return run_list


def get_absolute_url(job_url):
    host_url = utility_service.get_setting('HOST_URL')
    if host_url:
        return f"https://{host_url}{job_url}"
    else:
        context = util_context(utility_service.get_request())
        return f"{context['absolute_root_url']}{job_url}"


def get_endpoint_options():
    options = utility_service.recall()
    if options:
        return options

    log.trace()
    options = OrderedDict()
    try:
        eps = EndpointDefinition.objects.filter(app_code__in=get_app_codes()).order_by('title')
        for ep in eps:
            options[ep.id] = ep.title

    except Exception as ee:
        error_service.unexpected_error(
            "Unable to retrieve schedule-able jobs", ee
        )

    return utility_service.store(options)


def cleanup_run_records():
    # Max days should be a number, or False if app wants indefinite retention of history
    max_days = utility_service.get_setting('SCHEDULER_MAX_RECORD_AGE', 30)

    log.trace([max_days])
    if not max_days:
        return
    
    try:
        cutoff = datetime.now() - timedelta(days=max_days)
        num_deleted, _ = JobExecution.objects.filter(app_code__in=get_app_codes(), last_updated__lt=cutoff).delete()
        log.info(f"Deleted {num_deleted} JobExecution record(s) over {max_days} day(s) old")
    except Exception as ee:
        error_service.record(ee)
