"""CUSTOM MODULE TO WRITE GOOGLE SEARCH CONSOLE DATA"""
# pylint: disable=import-error, too-few-public-methods, unused-import
from datetime import datetime
from typing import Union, List, Any, Dict, Tuple, Optional
from sdc_dp_helpers.base_writers import BaseWriter


class GoogleSearchConsoleWriter(BaseWriter):
    """WRITER FOR Google Search Console RECRUIT DATA"""

    def verify_data(
        self, payload: Dict[str, Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:
        """verifies data before writting to destination also designs the destination file path

        Args:
            payload (Dict[str, Any]): expecting a dictionary having data, date and dimension

        Raises:
            KeyError: if we do not find the exact keys we expect from the payload
            TypeError: if provided data object is not a list

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: full destination path and
                                                                          data to be written
        """
        # confirm the payload keys are matching accurately with what is expected
        if not {"data", "date", "dimension"}.issubset(set(payload.keys())):
            raise KeyError("invalid payload expecting: data, date, dimension")

        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")

        try:
            datetime.strptime(payload["date"], "%Y%m%d")
        except ValueError as exc:
            raise ValueError(
                f"wrong date value expected format YYYYMMDD: {payload['dimension']}"
            ) from exc

        if not isinstance(payload["dimension"], str):
            raise TypeError(f"wrong 'dimension' value passed: {payload['dimension']}")

        data: list = payload["data"]
        date: str = payload["date"]
        dimension: str = payload["dimension"]

        write_path: str = f"{self.folder_path}/{dimension}/{date}"
        return write_path, data
