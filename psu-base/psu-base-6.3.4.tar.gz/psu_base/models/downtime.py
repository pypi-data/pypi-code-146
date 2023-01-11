from django.db import models
from psu_base.classes.ConvenientDate import ConvenientDate
from datetime import datetime


class Downtime(models.Model):
    """Downtime/MaintenanceWindow"""

    from_date = models.DateTimeField(blank=False, null=False)
    until_date = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def start_cd(self):
        return ConvenientDate(self.from_date)

    @property
    def end_cd(self):
        return ConvenientDate(self.until_date)

    @property
    def downtime_type(self):
        return "psu_base"

    def from_date_description(self):
        if self.from_date:
            return self.start_cd.humanized()
        else:
            return ""

    def from_date_display(self):
        if self.from_date:
            return self.start_cd.banner_date_time()
        else:
            return ""

    def until_date_display(self):
        if self.until_date:
            return self.end_cd.banner_date_time()
        else:
            return ""

    def minutes_until_start(self):
        now = datetime.now()
        if not self.is_future():
            return None
        return int((self.from_date - now).total_seconds() / 60.0)

    def is_past(self):
        return self.until_date < datetime.now()

    def is_future(self):
        return self.from_date > datetime.now()

    def is_active(self):
        if self.is_future():
            return False
        if self.is_past():
            return False
        return True

    def can_delete(self):
        # Can only delete future downtime records
        now = datetime.now()
        return self.is_future()

    def can_end(self):
        # Can only end current downtime records
        return self.is_active()

    @classmethod
    def get(cls, pk):
        """
        Get instance from ID
        """
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None
