#!/usr/bin/env python
"""CHIME/FRB Events API."""
import logging
from typing import Any, Dict, List, Union

from chime_frb_api.core import API

log = logging.getLogger(__name__)

INT_ARGS = [
    "beam_number",
    "nchain_end",
    "nchain_start",
    "nwalkers_end",
    "nwalkers_start",
    "dof",
]
STRING_ARGS = [
    "datetime",
    "timestamp_UTC_400MHz",
    "calibration_source_name",
    "calibration_source_date",
]
FLOAT_ARGS = [
    "dm",
    "dm_error",
    "dm_snr",
    "dm_snr_error",
    "dm_structure",
    "dm_structure_error",
    "width",
    "width_error",
    "snr",
    "delta_chi2",
    "drift_rate",
    "drift_rate_error" "dm_index",
    "dm_index_error",
    "timestamp_UTC_400MHz_error",
    "timestamp",
    "timestamp_error",
    "spectral_running",
    "spectral_running_error",
    "frequency_mean",
    "frequency_mean_error",
    "frequency_width",
    "frequency_width_error",
    "flux",
    "flux_error",
    "fluence",
    "fluence_error",
    "fitburst_reference_frequency",
    "fitburst_reference_frequency_scattering",
    "ftest_statistic",
    "scattering_index",
    "scattering_index_error",
    "scattering_timescale",
    "scattering_timescale_error",
    "linear_polarization_fraction",
    "linear_polarization_fraction_error",
    "circular_polarization_fraction",
    "circular_polarization_fraction_error",
    "spectral_index",
    "spectral_index_error",
    "rotation_measure",
    "rotation_measure_error",
    "redshift_host",
    "redshift_host_error",
    "dispersion_smearing",
    "dispersion_smearing_error",
    "spin_period",
    "spin_period_error",
    "ra",
    "ra_error",
    "dec",
    "dec_error",
    "gl",
    "gb",
    "system_temperature",
    "mb_bandwidth_mhz",
]
BOOL_ARGS = ["is_bandpass_calibrated"]
DICT_ARGS = ["galactic_dm", "pipeline", "fixed"]
LIST_ARGS = [
    "sub_burst_dm",
    "sub_burst_dm_error",
    "sub_burst_fluence",
    "sub_burst_fluence_error",
    "sub_burst_snr",
    "sub_burst_spectral_index",
    "sub_burst_spectral_index_error",
    "sub_burst_spectral_running",
    "sub_burst_spectral_running_error",
    "sub_burst_timestamp",
    "sub_burst_timestamp_error",
    "sub_burst_timestamp_UTC",
    "sub_burst_timestamp_UTC_error",
    "sub_burst_width",
    "sub_burst_width_error",
    "sub_burst_scattering_timescale",
    "sub_burst_scattering_timescale_error",
    "gain",
    "expected_spectrum",
    "multi_component_width",
    "multi_component_width_error",
    "pulse_emission_region",
    "pulse_start_bins",
    "pulse_end_bins",
    "sub_burst_flux",
    "sub_burst_flux_error",
    "sub_burst_fluence",
    "sub_burst_fluence_error",
    "sub_burst_start_bins",
    "sub_burst_end_bins",
    "ra_list",
    "ra_list_error",
    "dec_list",
    "dec_list_error",
    "x_list",
    "x_list_error",
    "y_list",
    "y_list_error",
    "max_log_prob",
    "chi2_list",
    "bw_low_frequencies_mhz",
    "bw_high_frequencies_mhz",
    "bw_chi2_reduced",
    "bw_rpl_fit",
]
VALID_ARGS = INT_ARGS + FLOAT_ARGS + BOOL_ARGS + DICT_ARGS + LIST_ARGS + STRING_ARGS


class Events:
    """CHIME/FRB Events API."""

    def __init__(self, API: API):
        """Initialize Events API."""
        self.API = API

    def get_event(self, event_number: int, full_header: bool = False) -> dict:
        """Get CHIME/FRB Event Information.

        Args:
            event_number: CHIME/FRB Event Number
            full_header: Get the full event from L4, default is False

        Returns:
            dict
        """
        if full_header:
            return self.API.get(f"/v1/events/full-header/{event_number}")
        else:
            return self.API.get(f"/v1/events/{event_number}")

    def get_all_events(self) -> list:
        """Get all CHIME/FRB Events from Events Database.

        Args:
            None

        Returns:
            list
        """
        return self.API.get("/v1/events")

    def get_file(self, filename: str) -> bytes:
        """Get a file from CHIME/FRB Backend.

        Args:
            filename: Filename on the CHIME/FRB Archivers

        Returns:
            Raw byte-encoded datastream

        Example:
            >>> response = master.frb_master.get_file('/some/file/name')
            >>> with open('filename.png', 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        """
        return self.API.stream(
            url="/v1/events/filename", request_type="POST", json={"filename": filename}
        )

    def add_measured_parameters(
        self,
        event_number: int,
        measured_parameters: Union[Dict[Any, Any], List[Dict[Any, Any]]],
    ) -> bool:
        """Append a new set of measured parameters to CHIME/FRB Event.

        Args:
            measured_parameters: [dict]
                list of a dictionary of measured parameters to update,
                valid values for each item in the list are
            pipeline: {
                    name: str
                        Name of the pipeline used to generate measured parameters
                    status: str
                        Status of the Pipeline
                            SCHEDULED
                            IN PROGRESS
                            COMPLETE
                            ERROR
                            UNKNOWN
                    log: str
                        Small message describing the pipeline run.
                    version:
                        version of the pipeline used to make the measured parameters
                }
                dm : float
                dm_error : float
                width : float
                width_error : float
                snr : float
                dm_index : float
                dm_index_error : float
                flux : float
                flux_error : float
                fluence : float
                fluence_error : float
                spectral_running : float
                spectral_running_error : float
                frequency_mean : float
                frequency_mean_error : float
                frequency_width : float
                frequency_width_error : float
                fitburst_reference_frequency : float
                fitburst_reference_frequency_scattering : float
                ftest_statistic : float
                is_bandpass_calibrated : bool
                fixed : dict
                sub_burst_dm : list
                sub_burst_dm_error : list
                sub_burst_fluence : list
                sub_burst_fluence_error : list
                sub_burst_snr : list
                sub_burst_spectral_index : list
                sub_burst_spectral_index_error : list
                sub_burst_spectral_running : list
                sub_burst_spectral_running_error : list
                sub_burst_timestamp : list
                sub_burst_timestamp_error : list
                sub_burst_timestamp_UTC : list
                sub_burst_timestamp_UTC_error : list
                sub_burst_width : list
                sub_burst_width_error : list
                sub_burst_scattering_timescale : list
                sub_burst_scattering_timescale_error : list
                scattering_index : float
                scattering_index_error : float
                scattering_timescale : float
                scattering_timescale_error : float
                linear_polarization_fraction : float
                linear_polarization_fraction_error : float
                circular_polarization_fraction : float
                circular_polarization_fraction_error : float
                spectral_index : float
                spectral_index_error : float
                rotation_measure : float
                rotation_measure_error : float
                redshift_host : float
                redshift_host_error : float
                dispersion_smearing : float
                dispersion_smearing_error : float
                spin_period : float
                spin_period_error : float
                ra : float
                ra_error : float
                dec : float
                dec_error : float
                gl : float
                gb : float
                system_temperature : float
                beam_number : int
                galactic_dm : dict
                gain : list
                expected_spectrum: list
                bw_low_frequencies_mhz: list
                bw_high_frequencies_mhz: list
                bw_chi2_reduced: list
                bw_rpl_fit: list
                mb_bandwidth_mhz: float

        Returns:
            db_response : dict
        """
        try:
            assert measured_parameters is not None, "measured parameters are required"
            if not isinstance(measured_parameters, list):
                measured_parameters = [measured_parameters]
            assert event_number is not None, "event_number is required"
            for item in measured_parameters:
                assert "pipeline" in item.keys(), "pipeline dictionary is required"
                assert "name" in item["pipeline"].keys(), "pipeline name is required"
                assert (
                    "status" in item["pipeline"].keys()
                ), "pipeline status is required"
                assert (
                    len(item.keys()) > 1
                ), "no parameters updated"  # pipeline is already 1 key
        except AssertionError as e:
            raise NameError(e)

        payloads = []
        try:
            for item in measured_parameters:
                payload = {}
                # Check if the args are valid
                for key, value in item.items():
                    assert key in VALID_ARGS, f"invalid parameter key <{key}>"
                    self._check_arg_type(key, value)
                    payload[key] = value
                payloads.append(payload)
            url = f"/v1/events/measured-parameters/{event_number}"
            response: bool = self.API.put(url=url, json=payloads)
            return response
        except AssertionError as e:
            raise NameError(e)
        except TypeError as e:
            raise TypeError(e)
        except Exception as e:
            raise e

    def _check_arg_type(self, key, value):
        try:
            if key in INT_ARGS:
                if not isinstance(value, int):
                    raise TypeError(key)
            if key in STRING_ARGS:
                if not isinstance(value, str):
                    raise TypeError(key)
            elif key in FLOAT_ARGS:
                if not isinstance(value, float):
                    raise TypeError(key)
            elif key in DICT_ARGS:
                if not isinstance(value, dict):
                    raise TypeError(key)
            elif key in LIST_ARGS:
                if not isinstance(value, list):
                    raise TypeError(key)
        except TypeError as e:
            log.error(e)
            raise TypeError(f"invalid parameter type <{key}, {value}>")
