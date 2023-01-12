from psu_base.classes.Log import Log
from functools import wraps
from django.http import HttpResponseForbidden
from psu_scheduler.models import JobExecution
from psu_base.services import auth_service, error_service

log = Log()


def scheduled_job():
    """
    Decorator for views that are executed as scheduled jobs
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            exe = None
            allowed = False

            job_id = request.GET.get('job_id')
            job_key = request.GET.get('job_key')

            # If the job ID and Key provided?
            if 'job_key' in request.GET and 'job_id' in request.GET:

                # Get the job execution record
                exe = JobExecution.get(job_id)
                # If not found, invalid key, or already ran - Log a message
                if not exe:
                    log.error(f"Scheduled job #{job_id} does not exist")
                elif exe.key != job_key:
                    log.error(f"Incorrect key for scheduled job #{job_id}: {job_key}")
                elif exe.status != 'init':
                    log.error(f"Scheduled job #{job_id} already ran")
                else:
                    log.info(f"Scheduled job #{job_id} is allowed to run")
                    allowed = True

            elif auth_service.has_authority('~SuperUser'):
                log.info(f"SuperUser {auth_service.get_user().display_name} is allowed to run scheduled jobs")
                allowed = True

            else:
                log.error(f"Scheduled job was called without providing an ID and Key")

            # Return Forbidden response if not allowed
            if not allowed:
                return HttpResponseForbidden('Job was not allowed to run')

            # Otherwise, render the view
            if exe:
                exe.status = 'run'
                exe.save()

                if exe.job.performer:
                    # ToDo: Fake authentication for performer, if specified
                    pass

            # Run the job
            response = None
            try:
                response = view_func(request, *args, **kwargs)
                exe_status = 'done'
            except Exception as ee:
                exe_status = 'error'
                error_service.record(ee, exe)

            if exe:
                # Update the Execution record
                exe.status = exe_status

                if hasattr(response, 'status_code'):
                    exe.http_status = response.status_code

                if hasattr(response, 'content'):
                    exe.output = response.content
                else:
                    exe.output = str(response)

                exe.save()

                log.info(f"Scheduled job #{job_id} completion status: {exe.http_status or exe_status}")
            else:
                log.info(f"Non-scheduled job completion status: {exe_status}")
            return response

        return _wrapped_view
    return decorator
