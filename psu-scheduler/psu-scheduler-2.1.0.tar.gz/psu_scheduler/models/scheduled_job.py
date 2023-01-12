from django.db import models
from psu_base.classes.Log import Log
from psu_base.classes.ConvenientDate import ConvenientDate
from collections import OrderedDict
from datetime import datetime, timedelta
from psu_base.services import utility_service
from .endpoint_definition import EndpointDefinition

log = Log()


class ScheduledJob(models.Model):
    """Jobs scheduled to run at specified days/times"""

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    app_code = models.CharField(
        max_length=15,
        verbose_name='Application Code',
        help_text='Application that this job belongs to.',
        blank=False, null=False, db_index=True
    )
    status_ind = models.CharField(
        max_length=1,
        blank=False, null=False, default='A'
    )

    endpoint = models.ForeignKey(EndpointDefinition, models.CASCADE, blank=False, null=False)

    performer = models.CharField(
        max_length=30,
        help_text='This holds the username of the job performer, if applicable',
        blank=True, null=True
    )

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # "0123456"
    run_days = models.CharField(
        max_length=7,
        blank=True, null=False, default=""
    )

    # Option #1: list of times to run
    # "HHMM,HHMM,HHMM,...
    run_times_csv = models.CharField(
        max_length=30,
        blank=True, null=False, default=""
    )
    # Option #2: Frequency (in minutes) within the day.
    # This can be paired with a single run_time to start from, or two run_times to start and end at
    run_frequency = models.IntegerField(
        blank=False, null=False, default=0
    )

    def start_cd(self):
        if self.start_date:
            return ConvenientDate(self.start_date)

    def end_cd(self):
        if self.end_date:
            return ConvenientDate(self.end_date)

    def run_times(self):
        """
        Get scheduled run times as a list of "HHMM"
        """
        times = None
        if self.run_times_csv:
            times = utility_service.csv_to_list(self.run_times_csv, convert_int=False)

        if self.run_frequency and self.run_frequency > 0 and self.run_frequency < 1440:
            start_hhmm = times[0] if times else '0000'
            start_hh = start_hhmm[:2]
            start_mm = start_hhmm[2:]
            end_hhmm = times[1] if times and len(times) == 2 else '2359'
            end_hh = int(end_hhmm[:2])
            end_mm = int(end_hhmm[2:])

            times = []
            now = datetime.now()
            start_day = now.day
            start_time = now.replace(hour=int(start_hh), minute=int(start_mm), second=0, microsecond=0)
            end_time = now.replace(hour=int(end_hh), minute=int(end_mm), second=0, microsecond=0)

            tt = start_time
            while tt.day == start_day and tt <= end_time:
                times.append(f"{tt.strftime('%H')}{tt.strftime('%M')}")
                tt = tt + timedelta(0, 60 * self.run_frequency)

        return times if times else []

    def run_times_display(self):
        rt = self.run_times()
        if rt:
            return [f"{x.rjust(4, '0')[:2]}:{x.rjust(4, '0')[2:]}" for x in rt]

    def run_time_range(self):
        times = self.run_times()
        if times:
            range = f"{self.run_time_display(times[0])} - {self.run_time_display(times[len(times)-1])}"
        else:
            range = None
        del times
        return range

    @staticmethod
    def run_time_display(time_string):
        return f"{time_string[:2]}:{time_string[2:]}"

    def is_active(self):
        return self.status_ind == 'A'

    def last_scheduled_time(self):
        """
        Get most-recent scheduled run time as "HHMM" or None
        """
        # No scheduled time when not activated
        if not self.is_active():
            return None

        now = datetime.now()
        # Only look for time if scheduled to run today
        if str(now.weekday()) not in self.run_days:
            return None
        elif self.start_date and self.start_date > now:
            return None
        elif self.end_date and self.end_date < now:
            return None

        now_time = f"{now.strftime('%H')}{now.strftime('%M')}"
        last_time = None
        for tt in self.run_times():
            if tt <= now_time:
                last_time = tt
            else:
                break

        return last_time

    @staticmethod
    def day_options(self):
        d = OrderedDict()
        d['0'] = 'Monday'
        d['1'] = 'Tuesday'
        d['2'] = 'Wednesday'
        d['3'] = 'Thursday'
        d['4'] = 'Friday'
        d['5'] = 'Saturday'
        d['6'] = 'Sunday'
        return d

    def executions(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.jobexecution_set.filter(date_created__gte=today)

    def should_run(self):
        last_schedule = self.last_scheduled_time()
        if not last_schedule:
            return False

        # For recorded job executions today
        for ii in self.executions():
            # If started on or after scheduled time
            if ii.started_at() >= last_schedule:
                return False

        # ToDo: BUG - Runs on every call for the first minute of every hour (?)
        log.debug(f"Has not run since {last_schedule}")
        return True

    def url(self):
        return self.endpoint.url()

    def get_validation_errors(self):
        log.trace()
        errors = []
        current_time = datetime.now()

        if not self.endpoint:
            errors.append("You must specify a job to run")

        if not self.run_days:
            errors.append("You must specify days for the job to run")

        # Require at least one of the two:
        if not (self.run_times or self.run_frequency):
            errors.append("You must specify run times or a frequency")

        if self.run_frequency:
            if self.run_times_csv and len(self.run_times()) > 2:
                errors.append("You must specify either a frequency or a list of times, not both")

        # Validate date range
        if self.start_date and current_time > self.start_date:
            errors.append("Start date should be defined today or in the future")

        if self.end_date and current_time > self.end_date:
            errors.append(f"End date should be defined today or in the future")

        if self.end_date and self.start_date and self.start_date > self.end_date:
            errors.append("Start date should be defined before end date")
        return errors

    @classmethod
    def get(cls, cls_id):
        try:
            return cls.objects.get(pk=cls_id)
        except cls.DoesNotExist:
            return None
