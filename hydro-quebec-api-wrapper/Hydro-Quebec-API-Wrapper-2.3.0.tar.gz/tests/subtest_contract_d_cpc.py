"""Contract D CPC tests module."""
import datetime

import pytest
from hydroqc.account import Account
from hydroqc.contract import ContractDCPC
from hydroqc.winter_credit.consts import (
    DEFAULT_EVENING_PEAK_END,
    DEFAULT_EVENING_PEAK_START,
    DEFAULT_MORNING_PEAK_END,
    DEFAULT_MORNING_PEAK_START,
)

from .tools import SkipIfBadRate, today, today_str, yesterday_str


class SubTestContractDCPC:
    """Contract D CPCtests class."""

    @SkipIfBadRate(["D"], "CPC")
    @pytest.mark.asyncio
    async def test_contract_d_cpc_specific(
        self, account: Account, contract: ContractDCPC
    ) -> None:
        """Test total hourly consumption stats."""
        assert contract.rate == "D"
        assert contract.rate_option == "CPC"

        assert (
            isinstance(contract.cp_current_bill, float)
            and contract.cp_current_bill >= 0
        )
        assert (
            isinstance(contract.cp_projected_bill, float)
            and contract.cp_projected_bill >= 0
        )
        assert (
            isinstance(contract.cp_daily_bill_mean, float)
            and contract.cp_daily_bill_mean >= 0
        )
        assert (
            isinstance(contract.cp_projected_total_consumption, int)
            and contract.cp_projected_total_consumption >= 0
        )
        assert (
            isinstance(contract.cp_kwh_cost_mean, float)
            and contract.cp_kwh_cost_mean >= 0
        )

        contract.set_preheat_duration(60)
        winter_credit = contract.winter_credit
        assert winter_credit.applicant_id == contract.applicant_id
        assert winter_credit.customer_id == account.customer_id
        assert winter_credit.contract_id == contract.contract_id

        assert (
            len(winter_credit.raw_data) == 0
        ), "Raw data should be empty, data not fetched yet"

        await winter_credit.refresh_data()

        assert winter_credit.winter_start_date.month == 12
        assert winter_credit.winter_start_date.day == 1
        assert winter_credit.winter_end_date.month == 3
        assert winter_credit.winter_end_date.day == 31
        assert len(winter_credit.peaks) > 0
        assert len(winter_credit.sonic) > 0
        assert len(winter_credit.critical_peaks) >= 0
        assert len(winter_credit.critical_peaks) <= len(winter_credit.peaks)
        assert winter_credit.cumulated_credit >= 0
        assert winter_credit.projected_cumulated_credit >= 0
        assert (
            winter_credit.projected_cumulated_credit >= winter_credit.cumulated_credit
        )

        if (
            today <= winter_credit.winter_start_date.date()
            or today >= winter_credit.winter_end_date.date()
        ):
            assert winter_credit.current_peak is None
        else:
            # We are in winter
            now = datetime.datetime.now().time()
            if (DEFAULT_MORNING_PEAK_START <= now <= DEFAULT_MORNING_PEAK_END) or (
                DEFAULT_EVENING_PEAK_START <= now <= DEFAULT_EVENING_PEAK_END
            ):
                assert (
                    winter_credit.current_peak is not None
                    and winter_credit.current_peak.start_date
                    in [p.start_date for p in winter_credit.peaks]
                )
            else:
                assert winter_credit.current_peak is None
        assert winter_credit.current_peak_is_critical in {None, True, False}
        assert winter_credit.current_state in {
            "critical_anchor",
            "anchor",
            "critical_peak",
            "peak",
            "normal",
        }

        assert isinstance(winter_credit.preheat_in_progress, bool)
        assert isinstance(winter_credit.is_any_critical_peak_coming, bool)
        assert isinstance(winter_credit.next_peak_is_critical, bool)
        assert winter_credit.next_critical_peak in [None] + winter_credit.critical_peaks
        if (
            today <= winter_credit.winter_start_date.date()
            or today >= winter_credit.winter_end_date.date()
        ):
            assert winter_credit.today_morning_peak is None
            assert winter_credit.today_evening_peak is None
            assert winter_credit.tomorrow_morning_peak is None
            assert winter_credit.tomorrow_evening_peak is None
            assert winter_credit.yesterday_morning_peak is None
            assert winter_credit.yesterday_evening_peak is None
            assert winter_credit.next_anchor is None
        else:
            # We are in winter
            assert (
                winter_credit.today_morning_peak is not None
                and winter_credit.today_morning_peak.start_date
                in [p.start_date for p in winter_credit.peaks]
            )
            assert (
                winter_credit.today_evening_peak is not None
                and winter_credit.today_evening_peak.start_date
                in [p.start_date for p in winter_credit.peaks]
            )
            assert (
                winter_credit.tomorrow_morning_peak is not None
                and winter_credit.tomorrow_morning_peak.start_date
                in [p.start_date for p in winter_credit.peaks]
            )
            assert (
                winter_credit.tomorrow_evening_peak is not None
                and winter_credit.tomorrow_evening_peak.start_date
                in [p.start_date for p in winter_credit.peaks]
            )
            assert (
                winter_credit.yesterday_morning_peak is not None
                and winter_credit.yesterday_morning_peak.start_date
                in [p.start_date for p in winter_credit.peaks]
            )
            assert (
                winter_credit.yesterday_evening_peak is not None
                and winter_credit.yesterday_evening_peak.start_date
                in [p.start_date for p in winter_credit.peaks]
            )
            assert (
                winter_credit.next_anchor is not None
                and winter_credit.next_anchor.start_date
                in [p.anchor.start_date for p in winter_credit.peaks]
            )

        # get_hourly_energy
        data_csv = await contract.get_hourly_energy(yesterday_str, today_str)
        first_line = next(data_csv)
        assert first_line == [
            "Contrat",
            "Date et heure",
            "kWh",
            "Code de consommation",
            "Température moyenne (°C)",
            "Code de température",
        ], "Bad get_hourly_energy CSV headers"

        # get_daily_energy
        data_csv = await contract.get_daily_energy(yesterday_str, today_str)
        first_line = next(data_csv)
        assert first_line == [
            "Contrat",
            "Tarif",
            "Date",
            "kWh",
            "Code de consommation",
            "Température moyenne (°C)",
            "Code de température",
        ], "Bad get_daily_energy CSV headers"

        # get_consumption_overview_csv
        data_csv = await contract.get_consumption_overview_csv()
        first_line = next(data_csv)
        assert first_line == [
            "Contract",
            "Rate",
            "Starting date",
            "Ending date",
            "Day",
            "Date and time of last reading",
            "kWh",
            "Amount ($)",
            "Meter-reading code",
            "Average $/day",
            "Average kWh/day",
            "kWh anticipated",
            "Amount anticipated ($)",
            "Average temperature (°C)",
        ], "Bad get_consumption_overview_csv CSV headers"
