from psu_base.services import error_service, validation_service
from psu_base.decorators import trace
from psu_base.classes.Finti import Finti
from psu_base.classes.ConvenientDate import ConvenientDate
from psu_base.classes.Log import Log
from datetime import datetime, timedelta

log = Log()


class Term:
    as_of_date = None
    code = None
    description = None
    start_date = None
    end_date = None
    reg_start_date = None

    def get_week_of_term(self):
        if not self.start_date:
            return None

        week_start = self.start_date
        week_start_cd = ConvenientDate(week_start)
        week_end = week_start_cd.get_next_specified_day("Sunday")
        today = self.as_of_date or datetime.now()

        if today < week_start:
            log.warning(f"{self.description} ({self.code}) has not yet started")
            return 0

        if today > self.end_date:
            log.warning(f"{self.description} ({self.code}) has ended")
            return 99

        weeks = []
        for ii in range(1, 52):
            weeks.append(week_start)

            # if today >= week_start and today <= week_end:
            if week_start <= today <= week_end:
                break

            week_start = week_end + timedelta(days=1)
            week_start_cd = ConvenientDate(week_start)
            week_end = week_start_cd.get_next_specified_day("Sunday")

        week_number = len(weeks)
        return week_number

    @trace(metrics=True)
    def __init__(self, term_selection=None, se_flag="S"):
        """
        Get the specified or current term.

        term_selection may be a term code or a date (string or instance).
        if null, the current term will be selected

        If getting current term or term as-of a date, specify the S/E flag just as in zskutil:
            - S: Term starts on start date (break counts toward previous term)
            - E: Term starts as soon as previous term ends (break counts toward next term)
        """
        try:
            term_code = None
            as_of_date = None

            if term_selection:
                if validation_service.is_term(str(term_selection)):
                    term_code = term_selection
                    as_of_date = None
                else:
                    term_code = None
                    as_of = ConvenientDate(term_selection)
                    as_of_date = as_of.datetime_instance
                    if not as_of_date:
                        log.warning(f"Invalid term selection date: {term_selection}")
                        return

            prev_term_dict = None
            term_dict = None
            next_term_dict = None
            min_term = term_code if term_code else "202100"
            finti_data = Finti().get(f"wdt/v1/sso_proxy/sis/terms?min_term={min_term}")

            for ff in finti_data:
                this_term_code = ff["term_code"]
                if term_code and term_code != this_term_code:
                    continue

                elif term_code and term_code == this_term_code:
                    term_dict = ff
                    break

                start_date = ConvenientDate(ff["term_start_date"]).datetime_instance
                end_date = ConvenientDate(ff["term_end_date"]).datetime_instance
                now = as_of_date if as_of_date else datetime.now()
                self.as_of_date = now

                # If term has ended
                if end_date <= now:
                    prev_term_dict = ff

                    # If term has started (but has not ended)
                elif start_date <= now:
                    term_dict = ff

                # if term has not yet started
                else:
                    next_term_dict = ff
                    break  # Only the nearest future term

            if not term_dict:
                if se_flag.upper() == "S":
                    term_dict = next_term_dict
                else:
                    term_dict = prev_term_dict

            if not term_dict:
                log.warning("Unable to find term data")

            else:
                self.code = term_dict.get("term_code")
                self.description = term_dict.get("term_desc")
                self.start_date = ConvenientDate(term_dict.get("term_start_date")).datetime_instance
                self.end_date = ConvenientDate(term_dict.get("term_end_date")).datetime_instance
                self.reg_start_date = term_dict.get("registration_start_date")
                if self.reg_start_date:
                    self.reg_start_date = ConvenientDate(
                        self.reg_start_date
                    ).datetime_instance

        except Exception as ee:
            error_service.record(ee)

    def __repr__(self):
        return f"<{self.code}: {self.description}>" if self.code else "<Term: Empty Object>"

    @classmethod
    def get_current(cls, se_flag="S"):
        """
        Get the current term.

        Specify the S/E flag just as in zskutil:
            - S: Term starts on start date (break counts toward previous term)
            - E: Term starts as soon as previous term ends (break counts toward next term)
        """
        return Term(None, se_flag)

    @classmethod
    def get(cls, term_selection=None, se_flag="S"):
        """
        Get a specified term.

        term_selection may be a term code or a date (string or instance).
        if null, the current term will be selected

        Specify the S/E flag just as in zskutil:
            - S: Term starts on start date (break counts toward previous term)
            - E: Term starts as soon as previous term ends (break counts toward next term)
        """

        return Term(term_selection, se_flag)
