"""HydroQC planned and not planned Outage module.

See:
    * https://www.hydroquebec.com/documents-donnees/donnees-ouvertes/pannes-interruptions.html
    * https://infopannes.solutions.hydroquebec.com/statut-adresse/
    * https://www.hydroquebec.com/data/loi-sur-acces/pdf/description-des-codes-interruption.pdf
"""
import datetime
import logging

from hydroqc.types import OutageCause, OutageStatus, OutageTyping


class Outage:
    """planned and not planned Outage class."""

    def __init__(self, raw_data: OutageTyping, logger: logging.Logger):
        """Outage constructor."""
        self._raw_data = raw_data
        self._logger = logger

    @property
    def id_(self) -> int:
        """Get outage unique ID."""
        return self._raw_data["idInterruption"]["noInterruption"]

    @property
    def start_date(self) -> datetime.datetime:
        """Get outage start date.

        Tries to use `dateDebutReport` key if exists, then falls back to `dateDebut` key.
        """
        start_date = self._raw_data.get("dateDebutReport", self._raw_data["dateDebut"])
        return datetime.datetime.fromisoformat(start_date)

    @property
    def end_date(self) -> datetime.datetime:
        """Get outage end date.

        Tries to use `dateFinReport` key if exists, then falls back to `dateFin` key.
        """
        end_date = self._raw_data.get(
            "dateFinEstimeeMax",
            self._raw_data.get("dateFinReport", self._raw_data["dateFin"]),
        )
        return datetime.datetime.fromisoformat(end_date)

    @property
    def cause(self) -> OutageCause:
        """Get outage cause."""
        try:
            return OutageCause(int(self._raw_data["codeCause"]))
        except ValueError:
            self._logger.warning(
                "Outage code cause `%s` is not a supported cause code",
                self._raw_data["codeCause"],
            )
            return OutageCause(0)

    @property
    def planned_duration(self) -> datetime.timedelta:
        """Get outage duration in minutes."""
        return datetime.timedelta(minutes=self._raw_data["dureePrevu"])

    @property
    def status(self) -> OutageStatus:
        """Get outage status."""
        return OutageStatus(self._raw_data.get("codeIntervention", "_"))

    @property
    def emergency_level(self) -> str | None:
        """Get outage status."""
        # TODO find what N and P means
        return self._raw_data.get("niveauUrgence")

    @property
    def is_planned(self) -> bool:
        """Is it a planned outage or not."""
        return self._raw_data["interruptionPlanifiee"]

    def __repr__(self) -> str:
        """Represent an outage."""
        return f"<Outage - {self.id_} - {self.start_date.isoformat()} - {self.status}>"
