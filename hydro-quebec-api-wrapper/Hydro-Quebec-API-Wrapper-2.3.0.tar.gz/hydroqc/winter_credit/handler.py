"""Winter credit processing."""
import datetime
import logging

from hydroqc.error import HydroQcWinterCreditError
from hydroqc.hydro_api.client import HydroClient
from hydroqc.winter_credit.consts import (
    DEFAULT_EVENING_PEAK_START,
    DEFAULT_MORNING_PEAK_START,
    DEFAULT_PRE_HEAT_DURATION,
    EST_TIMEZONE,
)
from hydroqc.winter_credit.peak import Anchor, Peak

from hydroqc.types import CriticalPeakDataTyping, WinterCreditDataTyping


def _now() -> datetime.datetime:
    """Get EST localized now datetime."""
    return EST_TIMEZONE.localize(datetime.datetime.now())


class WinterCreditHandler:
    """Winter Credit extra logic.

    This class supplements Hydro API data by providing calculated values for pre_heat period,
    anchor period detection as well as next event information.
    """

    # peaks: list[Peak]

    def __init__(
        self,
        applicant_id: str,
        customer_id: str,
        contract_id: str,
        hydro_client: HydroClient,
        logger: logging.Logger,
    ):
        """Winter Credit constructor."""
        self._no_partenaire_demandeur: str = applicant_id
        self._no_partenaire_titulaire: str = customer_id
        self._no_contrat: str = contract_id
        self._hydro_client: HydroClient = hydro_client
        self._logger: logging.Logger = logger

        self._raw_data: WinterCreditDataTyping = {}
        self._preheat_duration = DEFAULT_PRE_HEAT_DURATION
        self._is_enabled: bool = False

    # Basics
    @property
    def applicant_id(self) -> str:
        """Get applicant id."""
        return self._no_partenaire_demandeur

    @property
    def customer_id(self) -> str:
        """Get customer id."""
        return self._no_partenaire_titulaire

    @property
    def contract_id(self) -> str:
        """Get contract id."""
        return self._no_contrat

    def set_preheat_duration(self, duration: int) -> None:
        """Set preheat duration in minutes."""
        self._preheat_duration = duration

    # Fetch raw data
    async def refresh_data(self) -> None:
        """Get data from HydroQuebec web site."""
        self._logger.debug("Fetching data from HydroQuebec...")
        self._raw_data = await self._hydro_client.get_winter_credit(
            self.applicant_id, self.customer_id, self.contract_id
        )
        self._logger.debug("Data fetched from HydroQuebec...")
        # Ensure that peaks are sorted by date
        if self._raw_data["periodesEffacementsHivers"]:
            self._raw_data["periodesEffacementsHivers"][0][
                "periodesEffacementHiver"
            ].sort(key=lambda x: (x["dateEffacement"], x["heureDebut"]))

    @property
    def raw_data(self) -> WinterCreditDataTyping:
        """Return raw collected data."""
        return self._raw_data

    # Internals
    @property
    def _raw_critical_peaks(self) -> list[CriticalPeakDataTyping]:
        """Shortcut to get quickly critical peaks."""
        if self._raw_data["periodesEffacementsHivers"]:
            return self._raw_data["periodesEffacementsHivers"][0][
                "periodesEffacementHiver"
            ]
        return []

    def _set_peak_critical(self, peak: Peak) -> None:
        """Determine if the passed peak is critical or not, and save it to the object."""
        if peak.morning_evening.upper() == "EVENING":
            default_start_time_str = DEFAULT_EVENING_PEAK_START.strftime("%H:%M:%S")
        elif peak.morning_evening.upper() == "MORNING":
            default_start_time_str = DEFAULT_MORNING_PEAK_START.strftime("%H:%M:%S")
        else:
            raise HydroQcWinterCreditError("Bad morning_evening value")

        for critical_peak in self._raw_critical_peaks:
            critical_peak_date = datetime.datetime.strptime(
                critical_peak["dateEffacement"], "%Y-%m-%dT%H:%M:%S.%f%z"
            ).date()
            if (
                critical_peak_date == peak.day
                and critical_peak["heureDebut"] == default_start_time_str
            ):
                raw_stats = critical_peak.copy()
                peak.set_critical(raw_stats)
                return

    # general data
    @property
    def winter_start_date(self) -> datetime.datetime:
        """Get start date of the winter credits."""
        if not self._raw_data["periodesEffacementsHivers"]:
            today = datetime.date.today()
            if today.month >= 12:
                return datetime.datetime.strptime(
                    f"{today.year}-12-01T05:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            if today.month <= 3:
                return datetime.datetime.strptime(
                    f"{today.year-1}-12-01T05:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            # today.month > 4
            raise ValueError("Please fix me")
        return datetime.datetime.strptime(
            self._raw_data["periodesEffacementsHivers"][0]["dateDebutPeriodeHiver"],
            "%Y-%m-%dT%H:%M:%S.%f%z",
        )

    @property
    def winter_end_date(self) -> datetime.datetime:
        """Get end date of the winter credits."""
        if not self._raw_data["periodesEffacementsHivers"]:
            today = datetime.date.today()
            if today.month >= 12:
                return datetime.datetime.strptime(
                    f"{today.year+1}-03-31T04:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            if today.month <= 3:
                return datetime.datetime.strptime(
                    f"{today.year}-03-31T04:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            # today.month > 4
            raise ValueError("Please fix me")
        return datetime.datetime.strptime(
            self._raw_data["periodesEffacementsHivers"][0]["dateFinPeriodeHiver"],
            "%Y-%m-%dT%H:%M:%S.%f%z",
        )

    @property
    def cumulated_credit(self) -> float:
        """Get cumulated credits."""
        return round(sum(p["montantEffacee"] for p in self._raw_critical_peaks), 2)

    @property
    def projected_cumulated_credit(self) -> float:
        """Get projected_cumulated credits."""
        if self._raw_data["montantEffaceProjete"] == "":
            return 0.0
        try:
            return float(self._raw_data["montantEffaceProjete"])
        except ValueError as exp:
            raise HydroQcWinterCreditError("Bad cumulated credit raw value") from exp

    # Peaks data
    @property
    def peaks(self) -> list[Peak]:
        """List all peaks of the current winter."""
        return self._get_peaks()

    def _get_peaks(self) -> list[Peak]:
        """Get all peaks of the current winter."""
        current_date = self.winter_start_date
        delta = datetime.timedelta(days=1)
        peak_list: list[Peak] = []
        while current_date < self.winter_end_date:
            # Morning
            peak = Peak(
                current_date, "morning", preheat_duration=self._preheat_duration
            )
            self._set_peak_critical(peak)
            peak_list.append(peak)
            # Evening
            peak = Peak(
                current_date, "evening", preheat_duration=self._preheat_duration
            )
            self._set_peak_critical(peak)
            peak_list.append(peak)
            # Next day
            current_date += delta
        peak_list.sort(key=lambda x: x.start_date)
        return peak_list

    @property
    def sonic(self) -> list[Peak]:
        """Piaf's joke."""
        return self._get_peaks()

    @property
    def critical_peaks(self) -> list[Peak]:
        """Get all critical peaks of the current credits."""
        return [p for p in self.peaks if p.is_critical]

    # Current peak
    @property
    def current_peak(self) -> Peak | None:
        """Get current peak.

        Return None if no peak is currently running
        FIXME This could be USELESS
        """
        now = _now()
        peaks: list[Peak] = [p for p in self.peaks if p.start_date < now < p.end_date]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError("There is more than one current peak !")
        if len(peaks) == 1:
            return peaks[0]
        return None

    @property
    def current_peak_is_critical(self) -> bool | None:
        """Return True if the current peak is critical."""
        if self.current_peak:
            return bool(self.current_peak.is_critical)
        return None

    # In progress
    @property
    def current_state(self) -> str:
        """Get the current state of the winter credit handler.

        It returns critical_anchor, anchor, critical_peak, peak or normal
        This value should help for automation.
        """
        now = _now()
        current_anchors = [
            p.anchor
            for p in self.peaks
            if p.anchor.start_date < now < p.anchor.end_date
        ]
        if current_anchors and current_anchors[0].is_critical:
            return "critical_anchor"
        if current_anchors and not current_anchors[0].is_critical:
            return "anchor"

        current_peaks = [p for p in self.peaks if p.start_date < now < p.end_date]
        if current_peaks and current_peaks[0].is_critical:
            return "critical_peak"
        if current_peaks and not current_peaks[0].is_critical:
            return "peak"
        return "normal"

    @property
    def preheat_in_progress(self) -> bool:
        """Get the preheat state.

        Returns True if we have a preheat period is in progress.
        """
        now = _now()
        if self.next_peak is None:
            return False
        return self.next_peak.preheat.start_date < now < self.next_peak.preheat.end_date

    # Upcoming
    @property
    def is_any_critical_peak_coming(self) -> bool:
        """Get critical state of the upcoming events.

        It will return True if one of the "not completed yet" peak is critical.

        Retourne True si au moins un des prochains peaks non terminés est critical.
        """
        return bool(self.next_critical_peak)

    # Next peak
    @property
    def next_peak(self) -> Peak | None:
        """Get next peak or current peak."""
        return self._get_next_peak()

    def _get_next_peak(self) -> Peak | None:
        """Get next peak or current peak."""
        now = _now()
        peaks: list[Peak] = [p for p in self.peaks if now < p.end_date]
        if not peaks:  # pylint: disable=consider-using-assignment-expr
            return None
        next_peak = min(peaks, key=lambda x: x.start_date)
        return next_peak

    @property
    def next_peak_is_critical(self) -> bool:
        """Return True if the following next peak is critical.

        This method is quite useless because, to call this attribute

        * we need to write::

            contract.winter_credit.next_peak_is_critical

        * but it equivalent to::

            contract.winter_credit.next_peak.is_critical

        """
        if (next_peak := self._get_next_peak()) is None:
            return False
        return next_peak.is_critical

    @property
    def next_critical_peak(self) -> Peak | None:
        """Get next peak or current peak."""
        now = _now()
        peaks: list[Peak] = [p for p in self.critical_peaks if now < p.end_date]
        if not peaks:  # pylint: disable=consider-using-assignment-expr
            return None
        next_peak = min(peaks, key=lambda x: x.start_date)
        return next_peak

    # Today peaks
    @property
    def today_morning_peak(self) -> Peak | None:
        """Get the peak of today morning."""
        now = _now()
        peaks: list[Peak] = [
            p for p in self.peaks if p.day == now.date() and p.is_morning
        ]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError(
                "There is more than one morning peak today !"
            )
        if len(peaks) == 1:
            return peaks[0]
        return None

    @property
    def today_evening_peak(self) -> Peak | None:
        """Get the peak of today evening."""
        now = _now()
        peaks: list[Peak] = [
            p for p in self.peaks if p.day == now.date() and p.is_evening
        ]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError(
                "There is more than one evening peak today !"
            )
        if len(peaks) == 1:
            return peaks[0]
        return None

    # Tomorrow Peaks
    @property
    def tomorrow_morning_peak(self) -> Peak | None:
        """Get the peak of tomorrow morning."""
        now = _now()
        peaks: list[Peak] = [
            p
            for p in self.peaks
            if p.day == now.date() + datetime.timedelta(days=1) and p.is_morning
        ]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError(
                "There is more than one morning peak tomorrow !"
            )
        if len(peaks) == 1:
            return peaks[0]
        return None

    @property
    def tomorrow_evening_peak(self) -> Peak | None:
        """Get the peak of tomorrow evening."""
        now = _now()
        peaks: list[Peak] = [
            p
            for p in self.peaks
            if p.day == now.date() + datetime.timedelta(days=1) and p.is_evening
        ]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError(
                "There is more than one evening peak tomorrow !"
            )
        if len(peaks) == 1:
            return peaks[0]
        return None

    # Yesterday peaks
    @property
    def yesterday_morning_peak(self) -> Peak | None:
        """Get the peak of yesterday morning."""
        now = _now()
        peaks: list[Peak] = [
            p
            for p in self.peaks
            if p.day == now.date() - datetime.timedelta(days=1) and p.is_morning
        ]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError(
                "There is more than one morning peak yesterday !"
            )
        if len(peaks) == 1:
            return peaks[0]
        return None

    @property
    def yesterday_evening_peak(self) -> Peak | None:
        """Get the peak of yesterday evening."""
        now = _now()
        peaks: list[Peak] = [
            p
            for p in self.peaks
            if p.day == now.date() - datetime.timedelta(days=1) and p.is_evening
        ]
        if len(peaks) > 1:
            raise HydroQcWinterCreditError(
                "There is more than one evening peak yesterday !"
            )
        if len(peaks) == 1:
            return peaks[0]
        return None

    # Anchors
    @property
    def next_anchor(self) -> Anchor | None:
        """Next or current anchor."""
        now = _now()
        anchors: list[Anchor] = [
            p.anchor for p in self.peaks if now < p.anchor.end_date
        ]
        if anchors:
            next_anchor: Anchor = min(anchors, key=lambda x: x.start_date)
            return next_anchor
        return None
