from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.classes.ConvenientDate import ConvenientDate
from psu_scheduler.services import scheduler_service
from psu_base.services import utility_service, message_service, auth_service, error_service
from psu_base.decorators import require_authority, require_authentication
from requests_futures.sessions import FuturesSession
from psu_scheduler.models import ScheduledJob, JobExecution, EndpointDefinition
from psu_scheduler.decorators import scheduled_job
from django.core.paginator import Paginator
import secrets
import string
import re
import datetime

log = Log()


@scheduled_job()
def test_job(request):
    """A test job that does nothing"""
    log.trace()
    return HttpResponse('The test job has completed.')


def run_jobs_from_aws_health_check(request):
    """
    Run any scheduled jobs
    """
    log.trace()
    result = scheduler_service.call_jobs_via_finti()
    return HttpResponse(result)


def run_jobs(request):
    """
    Run any scheduled jobs
    """
    log.trace()
    jobs = scheduler_service.get_jobs_to_run()
    num_run = 0
    if jobs:
        executions = []
        session = FuturesSession()

        for job in jobs:
            # Record that job is running
            je = JobExecution()
            je.job = job
            je.key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            je.save()

            # ToDo: Max retries exceeded with url: /export/models?job_id=2&job_key=98IHK4H...
            relative_url = job.url()
            absolute_url = scheduler_service.get_absolute_url(relative_url)
            parameters = f"?job_id={je.id}&job_key={je.key}"

            call_url = f"{absolute_url}{parameters}"
            redirect_url = f"{relative_url}{parameters}"

            try:
                # Start job in background
                log.info(f"Calling: {call_url}")
                session.get(call_url)
                num_run += 1
            except:
                # AWS Health Check seems unable to make requests.  Maybe it can redirect instead?
                log.warning("Unable to call job. Redirecting to it instead")
                try:
                    return redirect(redirect_url)
                except:
                    log.warning("Unable to redirect to job.")

    scheduler_service.cleanup_run_records()
    return HttpResponse(f"Ran {num_run} jobs")


@require_authority('~SuperUser')
def endpoint_list(request):
    """
    List of defined endpoints (manage schedule-able jobs)
    """
    sort, page = utility_service.pagination_sort_info(request, 'title')
    endpoints = EndpointDefinition.objects.filter(app_code__in=scheduler_service.get_app_codes()).order_by(*sort)

    return render(request, 'psu_scheduler/endpoints.html', {'endpoints': endpoints})


@require_authority('~SuperUser')
def save_endpoint(request):
    """
    Create a new endpoints (schedule-able job)
    """

    title = request.POST.get('title')
    endpoint = request.POST.get('endpoint')

    job = EndpointDefinition()
    job.app_code = utility_service.get_app_code()
    job.title = title[:80]
    job.endpoint = endpoint[:200]
    job.save()

    return redirect('scheduler:endpoints')


@require_authority('~PowerUser')
def job_list(request):
    """
    List of defined jobs (manage schedules)
    """
    sort, page = utility_service.pagination_sort_info(request, 'endpoint__title')
    jobs = ScheduledJob.objects.filter(app_code__in=scheduler_service.get_app_codes()).order_by(*sort)
    endpoint_options = scheduler_service.get_endpoint_options()

    return render(request, 'psu_scheduler/scheduled_jobs.html', {'jobs': jobs, 'endpoint_options': endpoint_options})


@require_authority('~PowerUser')
def save_job(request):
    """
    Create a new scheduled job
    """
    log.trace()
    app_code = utility_service.get_app_code()

    # ToDo: Get endpoint from new table

    endpoint_id = request.POST.get('endpoint')
    endpoint = EndpointDefinition.get(endpoint_id) if endpoint_id else None
    if not endpoint:
        message_service.post_error("You must specify a valid job to run")
        return redirect('scheduler:jobs')

    run_times_csv = request.POST.get('run_times_csv')
    run_frequency = request.POST.get('run_frequency')
    if not run_frequency:
        run_frequency = 0

    # get run days as a string
    run_days = request.POST.getlist('run_days')
    run_days = ''.join(sorted([day for day in list(set(run_days)) if day in '0123456'])) if run_days else None

    # Validate run times
    if run_times_csv and ':' in run_times_csv:
        run_times_csv = run_times_csv.replace(':', '')
    run_times = utility_service.csv_to_list(run_times_csv)
    validated_times = []
    if run_times:
        for hhmm in run_times:
            hhmm = hhmm.rjust(4, '0')
            if re.match(r'^[012]\d[012345]\d$', hhmm):
                validated_times.append(hhmm)
            else:
                message_service.post_error(f"Invalid run time: {hhmm}")
    run_times_csv = ','.join(validated_times)
    del validated_times
    del run_times

    if run_frequency and not str(run_frequency).isnumeric():
        message_service.post_error("Run frequency must be a number of minutes")
        run_frequency = 0

    # Optional parameters:
    start_date = request.POST.get('start_date')
    if start_date:
        start_date = ConvenientDate(start_date).datetime_instance

    end_date = request.POST.get('end_date')
    if end_date:
        end_date = ConvenientDate(end_date).datetime_instance

    performer = request.POST.get('performer')
    if performer:
        job_user = auth_service.look_up_user_cache(performer)
        if job_user:
            performer = job_user.username
        else:
            performer = None
            message_service.post_error(f"Unknown job performer: {performer}")

    job = ScheduledJob()
    job.app_code = app_code
    job.endpoint = EndpointDefinition.get(endpoint_id)
    job.performer = performer if performer else None
    job.start_date = start_date if start_date else None
    job.end_date = end_date if end_date else None
    job.run_days = run_days
    job.run_times_csv = run_times_csv
    job.run_frequency = int(run_frequency) if run_frequency else 0

    errors = job.get_validation_errors()
    if errors:
        for ee in errors:
            message_service.post_error(ee)
    else:
        job.save()

    return redirect('scheduler:jobs')


@require_authority('~PowerUser')
def update_job(request):
    """
    Update the scheduled job
    """
    prop = request.POST.get('prop')
    value = request.POST.get('value')
    log.trace([prop, value])

    # Get job schedule record
    update_row = ScheduledJob.get(request.POST.get('id'))
    if not update_row:
        message_service.post_error("Could not find specified job")
        return HttpResponseForbidden()

    errors = False
    current_time = datetime.datetime.now()

    if prop == 'performer':
        value = request.POST.get('value')
        job_user = auth_service.look_up_user_cache(value)
        if job_user.username:
            update_row.performer = job_user.username
        else:
            errors = True
            message_service.post_error(f"Unknown job performer: {value}")

    elif prop == 'end_date':
        value = request.POST.get('value')
        end_date = None

        # Validate end date
        if value:
            end_date = ConvenientDate(value).datetime_instance
            if not end_date:
                errors = True
                message_service.post_error(f"Invalid end date was given")

            elif end_date and current_time > end_date:
                errors = True
                message_service.post_error(f"End date should be defined today or in the future")
            elif end_date and update_row.start_date and update_row.start_date > end_date:
                errors = True
                message_service.post_error("Start date should be defined before end date")

        update_row.end_date = end_date

    elif prop == 'run_days':
        value = request.POST.getlist('value[]')
        run_days = ''.join(sorted([day for day in list(set(value)) if day in '0123456'])) if value else None
        log.info(f'Updating run days from {update_row.run_days} to {run_days}')
        update_row.run_days = run_days

    elif prop == 'run_times':
        run_times_csv = request.POST.get('value')

        # Validate run times
        if update_row.run_frequency == 0 and not run_times_csv:
            message_service.post_error("Frequency or Run times must be defined")
            errors = True

        if run_times_csv and ':' in run_times_csv:
            run_times_csv = run_times_csv.replace(':', '')

        # A range of times is really just a list of two times
        if run_times_csv and '-' in run_times_csv:
            is_range = True
            run_times_csv = run_times_csv.replace('-', ',')
        else:
            is_range = False

        run_times = utility_service.csv_to_list(run_times_csv)
        validated_times = []

        if run_times:
            for hhmm in run_times:
                hhmm = hhmm.rjust(4, '0')
                if re.match(r'^[012]\d[012345]\d$', hhmm):
                    validated_times.append(hhmm)
                else:
                    message_service.post_error(f"Invalid run time: {hhmm}")
                    errors = True
            if len(run_times) > 2:
                update_row.run_frequency = 0
            elif is_range and not update_row.run_frequency:
                # Default 5 minute frequency for new time ranges
                update_row.run_frequency = 5

        run_times_csv = ','.join(validated_times)
        del validated_times
        del run_times
        update_row.run_times_csv = run_times_csv

    elif prop == 'run_frequency':
        run_frequency = request.POST.get('value')

        # Validate run frequency
        if run_frequency and int(run_frequency) > 1440:
            message_service.post_error("Frequency must be in minutes within a day")
            errors = True
        if not update_row.run_times_csv and (not run_frequency or run_frequency == str(0)):
            message_service.post_error("Frequency or Run times must be defined")
            errors = True
        if run_frequency and not str(run_frequency).isnumeric():
            message_service.post_error("Run frequency must be a number of minutes")
            run_frequency = 0
            errors = True

        update_row.run_frequency = int(run_frequency) if run_frequency else 0

        # If a frequency was defined, ensure run_times contains 0, 1, or 2 times
        if update_row.run_frequency:
            times = utility_service.csv_to_list(update_row.run_times_csv)
            if len(times) > 2:
                # Use first and last times as the range
                update_row.run_times_csv = f"{times[0]},{times[len(times)-1]}"

    if errors:
        return HttpResponseForbidden()

    else:
        update_row.save()
        message_service.post_success("Schedule has been updated.")
        return render(request, 'psu_scheduler/_schedule_job_tr.html', {
            'job': update_row
        })


@require_authority('~PowerUser')
def toggle_job_status(request, job_id):
    """
    Toggle a scheduled job's status Enabled/Disabled
    """
    log.trace()
    try:
        job = ScheduledJob.get(job_id)
        if job:
            if job.is_active():
                job.status_ind = 'I'
            else:
                job.status_ind = 'A'
            job.save()
    except Exception as ee:
        error_service.unexpected_error("Unable to change job status", ee)

    return redirect('scheduler:jobs')


@require_authority('~SuperUser')
def delete_job(request, job_id):
    """
    Delete a scheduled job
    """
    log.trace()
    try:
        job = ScheduledJob.get(job_id)
        if job:
            job.delete()
    except Exception as ee:
        error_service.unexpected_error("Unable to delete job", ee)

    return redirect('scheduler:jobs')


@require_authority('~PowerUser')
def executions(request):
    """Show details of job executions"""
    sort, page, filters = utility_service.pagination_sort_info(
        request, 'date_created', 'desc', ['endpoint', 'schedule']
    )

    if filters['endpoint']:
        job = EndpointDefinition.get(filters['endpoint'])
        exes = JobExecution.objects.filter(job__endpoint__id=filters['endpoint']).order_by(*sort)
    elif filters['schedule']:
        schedule = ScheduledJob.get(filters['schedule'])
        job = schedule.endpoint if schedule else None
        exes = JobExecution.objects.filter(job__id=filters['schedule']).order_by(*sort)
    else:
        job = None
        exes = []

    if exes:
        paginator = Paginator(exes, 50)
        exes = paginator.get_page(page)

    endpoint_options = scheduler_service.get_endpoint_options()

    return render(
        request, 'psu_scheduler/executions.html',
        {
            'endpoint_definition': job,
            'executions': exes,
            'endpoint_options': endpoint_options
        }
    )


@require_authority('~SuperUser')
def delete_endpoint(request, endpoint_id):
    """
    Delete a scheduled job
    """
    log.trace()
    try:
        endpoint = EndpointDefinition.get(endpoint_id)
        if endpoint:
            endpoint.delete()
    except Exception as ee:
        error_service.unexpected_error("Unable to delete endpoint", ee)

    return redirect('scheduler:endpoints')


@require_authority('~SuperUser')
def update_endpoint(request):
    """
    Update the endpoints
    """

    prop = request.POST.get('prop')
    update_row = EndpointDefinition.get(request.POST.get('id'))
    value = request.POST.get('value')
    if prop == 'title':
        update_row.title = value
    if prop == 'endpoint':
        update_row.endpoint = value
    update_row.save()
    return render(
        request, 'psu_scheduler/_endpoint_tr.html', {
            'endpoint': update_row
        }
    )