from psu_base.services import error_service
from psu_base.classes.ConvenientDate import ConvenientDate
from psu_base.classes.Log import Log
from datetime import datetime

log = Log()


class BannerDowntime:
    start_cd = None
    end_cd = None
    reason = None
    environment = None
    message = None
    downtime_type = "banner"
    finti_content = None

    @property
    def is_fye(self):
        return self.reason and self.reason.upper() == "FYE"

    def is_prod_downtime(self):
        return self.environment and self.environment.lower() in ["prod", "oprd", "production"]

    def minutes_until_start(self):
        """
        Returns: Minutes until start of downtime
                 - will be negative for past/active downtimes
        """
        diff = self.from_date - datetime.now()
        return int(diff.total_seconds() / 60)

    def minutes_since_start(self):
        """
        Returns: Minutes since start of downtime
                 - will be negative for future downtimes
        """
        diff = datetime.now() - self.from_date
        return int(diff.total_seconds() / 60)

    def from_date_description(self):
        if self.is_valid_downtime():
            return self.start_cd.humanized()

    def from_date_display(self):
        if self.is_valid_downtime():
            return self.start_cd.banner_date_time()

    def until_date_display(self):
        if self.is_valid_downtime():
            return self.end_cd.banner_date_time()

    def until_time_display(self):
        date_str = ""
        if self.until_date.date() != self.from_date.date():
            date_str = self.end_cd.format("MMMM DD")
        time_str = self.end_cd.format("hh:mm a")
        return f"{date_str} at {time_str}".strip()

    @property
    def from_date(self):
        if self.is_valid_downtime():
            return self.start_cd.datetime_instance

    @property
    def until_date(self):
        if self.is_valid_downtime():
            return self.end_cd.datetime_instance

    def is_past(self):
        return self.until_date < datetime.now()

    def is_future(self):
        return self.from_date > datetime.now()

    def is_active(self):
        return not (self.is_past() or self.is_future())

    def is_valid_downtime(self):
        try:
            # Start and end times are required
            if not self.start_cd.datetime_instance:
                return False
            if not self.end_cd.datetime_instance:
                return False
        except Exception as ee:
            error_service.record(ee)
            return False
        return True

    def __init__(self, finti_dict):
        try:
            if finti_dict:
                self.finti_content = finti_dict
                self.start_cd = ConvenientDate(finti_dict.get("downtime_beg"))
                self.end_cd = ConvenientDate(finti_dict.get("downtime_end"))
                self.reason = finti_dict.get("downtime_type")
                self.environment = finti_dict.get("environment")
                self.message = finti_dict.get("message")
        except Exception as ee:
            error_service.record(ee)

    def __repr__(self):
        return f"{self.reason}: {self.start_cd} - {self.end_cd}"
