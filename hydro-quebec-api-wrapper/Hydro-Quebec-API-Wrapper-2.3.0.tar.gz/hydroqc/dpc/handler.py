"""Winter credit processing."""
import datetime
import logging

from hydroqc.dpc.consts import DEFAULT_PRE_HEAT_DURATION, EST_TIMEZONE
from hydroqc.dpc.peak import Peak
from hydroqc.error import HydroQcDPCPeakError
from hydroqc.hydro_api.client import HydroClient

from hydroqc.types import DPCPeakDataTyping, DPCPeakListDataTyping


def _now() -> datetime.datetime:
    """Get EST localized now datetime."""
    return EST_TIMEZONE.localize(datetime.datetime.now())


class DPCPeakHandler:
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

        self._raw_data: list[DPCPeakDataTyping] = []
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
    async def refresh_data(self) -> DPCPeakListDataTyping:
        """Get data from HydroQuebec web site."""
        self._logger.debug("Fetching data from HydroQuebec...")
        _raw_data = await self._hydro_client.get_dpc_peak_data(
            self.applicant_id, self.customer_id, self.contract_id
        )

        self._logger.debug("Data fetched from HydroQuebec...")
        # Ensure that peaks are sorted by date
        self._raw_data = []
        if _raw_data["listePeriodePointeCritiqueAujourdhui"]:
            self._raw_data += _raw_data["listePeriodePointeCritiqueAujourdhui"]
        if _raw_data["listePeriodePointeCritiqueDemain"]:
            self._raw_data += _raw_data["listePeriodePointeCritiqueDemain"]

        self._raw_data.sort(key=lambda x: x["dateDebut"])
        return _raw_data

    @property
    def raw_data(self) -> list[DPCPeakDataTyping]:
        """Return raw collected data."""
        return self._raw_data

    # Internals

    # general data
    @property
    def winter_start_date(self) -> datetime.datetime:
        """Get start date of the winter credits."""
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

    @property
    def winter_end_date(self) -> datetime.datetime:
        """Get end date of the winter credits."""
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

    # Peaks data
    @property
    def peaks(self) -> list[Peak]:
        """List all peaks of the current winter."""
        return self._get_peaks()

    def _get_peaks(self) -> list[Peak]:
        """Get all peaks of the current winter."""
        peak_list: list[Peak] = []
        for raw_peak in self._raw_data:
            peak = Peak(
                datetime.datetime.fromisoformat(raw_peak["dateDebut"]),
                datetime.datetime.fromisoformat(raw_peak["dateFin"]),
                preheat_duration=self._preheat_duration,
            )
            peak_list.append(peak)

        peak_list.sort(key=lambda x: x.start_date)
        return peak_list

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
            raise HydroQcDPCPeakError("There is more than one current peak !")
        if len(peaks) == 1:
            return peaks[0]
        return None

    # In progress
    @property
    def current_state(self) -> str:
        """Get the current state of the winter credit handler.

        It returns peak or normal
        This value should help for automation.
        """
        now = _now()
        if [p for p in self.peaks if p.start_date < now < p.end_date]:
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

    # Today peaks
    @property
    def today_morning_peak(self) -> Peak | None:
        """Get the peak of today morning."""
        now = _now()
        peaks: list[Peak] = [
            p for p in self.peaks if p.date == now.date() and p.start_date.hour < 12
        ]
        if len(peaks) > 1:
            raise HydroQcDPCPeakError("There is more than one morning peak today !")
        if len(peaks) == 1:
            return peaks[0]
        return None

    @property
    def today_evening_peak(self) -> Peak | None:
        """Get the peak of today evening."""
        now = _now()
        peaks: list[Peak] = [
            p for p in self.peaks if p.date == now.date() and p.start_date.hour > 12
        ]
        if len(peaks) > 1:
            raise HydroQcDPCPeakError("There is more than one evening peak today !")
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
            if p.date == now.date() + datetime.timedelta(days=1)
            and p.start_date.hour < 12
        ]
        if len(peaks) > 1:
            raise HydroQcDPCPeakError("There is more than one morning peak tomorrow !")
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
            if p.date == now.date() + datetime.timedelta(days=1)
            and p.start_date.hour > 12
        ]
        if len(peaks) > 1:
            raise HydroQcDPCPeakError("There is more than one evening peak tomorrow !")
        if len(peaks) == 1:
            return peaks[0]
        return None
