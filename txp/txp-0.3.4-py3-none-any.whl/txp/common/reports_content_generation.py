from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from PIL import Image
import pandas as pd


class ReportSection(ABC):

    def __init__(
        self,
        tenant_id: str,
        asset_id: str,
        header: Optional[str] = None,
    ):
        pass

    @abstractmethod
    def required_inputs(self) -> List["SectionInputsEnum"]:
        pass

    @abstractmethod
    def compute_section(self, **kwargs):
        pass

    @abstractmethod
    def section_name(self) -> str:
        pass

    @abstractmethod
    def get_persisted_section(self, path: str):
        pass

    @abstractmethod
    @property
    def value(self):
        pass


# Strong typing for the possible value outputs
class ImageReportSection(ReportSection, ABC):
    def __init__(
        self,
        tenant_id: str,
        asset_id: str,
        header: Optional[str] = None,
    ):
        super(ImageReportSection, self).__init__(
            tenant_id, asset_id, header
        )
        self._image: Image = None

    def get_persisted_section(self, path: str):
        # obtain de object from persistence
        object = {}
        image_file = path + object['value']
        self._image = Image(image_file)

    def value(self):
        return self._image


class NumericReportSection(ReportSection, ABC):
    def __init__(
        self,
        tenant_id: str,
        asset_id: str,
        value: Optional[int] = 0,
        header: Optional[str] = None,
    ):
        super(NumericReportSection, self).__init__(
            tenant_id, asset_id, value, header
        )


# Framework Client will create concrete types for the desired sections
class EventsForecastingSection(ImageReportSection):
    def __init__(
        self,
        tenant_id: str,
        asset_id: str,
        value: Optional[Image] = None,
        header: Optional[str] = None,
    ):
        super(EventsForecastingSection, self).__init__(
            tenant_id, asset_id, value, header
        )

    def required_inputs(self) -> List["SectionInputsEnum"]:
        return ["EventsData"]

    def compute_section(self, **kwargs):
        pass



class StatesDistributionSection(ImageReportSection):
    def __init__(
        self,
        tenant_id: str,
        asset_id: str,
        value: Optional[Image] = None,
        header: Optional[str] = None,
    ):
        super(StatesDistributionSection, self).__init__(
            tenant_id, asset_id, value, header
        )

    def required_inputs(self) -> List["SectionInputsEnum"]:
        return ["StatesData"]

    def compute_section(self, **kwargs):
        pass


class StatesVariatonRate(NumericReportSection):
    def __init__(
        self,
        tenant_id: str,
        asset_id: str,
        value: Optional[Image] = None,
        header: Optional[str] = None,
    ):
        super(StatesVariatonRate, self).__init__(
            tenant_id, asset_id, value, header
        )

    def required_inputs(self) -> List["SectionInputsEnum"]:
        return ["StatesData"]

    def compute_section(self, **kwargs):
        pass


class BaseReportContent(ABC):
    """Base class to encapsulate all the data download/persistence
    operations for the ReportContents children."""

    def __init__(
        self,
        report_section: List[ReportSection],
        report_coordinates: "ReportCoordinates"
    ):
        self._sections: List[ReportSection] = report_section
        self._report_coordinates: "ReportCoordinates" = report_coordinates

        self._time_raw_data: pd.DataFrame = None
        self._fft_data: pd.DataFrame = None
        self._psd_data: pd.DataFrame = None
        self._metrics_data: pd.DataFrame = None
        self._events_data: pd.DataFrame = None
        self._states_data: pd.DataFrame - None

        if self._available():
            self.load()

    def _available(self) -> bool:
        pass

    def _load(self) -> None:
        pass

    def download_tabular_data(self):
        """This method should visit the sections and check which data requires to
        download in order to inject the data to the sections."""
        pass

    def compute_sections(self):
        """Here we can request the """
        self._donwload_tabular_data()

        # Here we should perform some kind of decision on the current section
        # to inject the required data.
        for section in self._sections:
            section.compute_section()

    def _get_persisted_object(self) -> Dict:
        d = {}
        for section in self._sections:
            d[section.section_name()] = section.get_persisted_object_value()

    def _write_to_persistence_layer(self) -> None:
        print("This is not the DB you're looking for ... ")
        pass

    def save(self) -> None:
        persisted_obj = self._get_persisted_object()
        """In this point, we will save the persisted object form."""
        self._write_to_persistence_layer(persisted_obj)

        for section in self._sections:
            section.save_resources()

