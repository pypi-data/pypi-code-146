from datetime import datetime

from perun.connector.utils.Logger import Logger
from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import ResponseMicroService

logger = Logger.get_logger(__name__)


class IsEligible(ResponseMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("IsEligible is active")

        self.__TARGET_ATTRIBUTES = "target_attributes"
        self.__DEFAULT_TARGET_ATTRIBUTES = ["eduPersonAssurance"]
        self.__ELIGIBILITY_TIMESTAMPS_DICT_ATTRIBUTE = (
            "eligibility_timestamps_dict_attribute"
        )
        self.__SUPPORTED_ELIGIBILITY_TYPES = "supported_eligibility_types"

        self.__target_attributes = config.get(self.__TARGET_ATTRIBUTES)
        self.__eligibility_timestamps_dict_attribute = config.get(
            self.__ELIGIBILITY_TIMESTAMPS_DICT_ATTRIBUTE
        )

        self.__supported_eligibility_types = config.get(
            self.__SUPPORTED_ELIGIBILITY_TYPES
        )

    def process(self, context: Context, data: InternalData):
        """
        Obtains dict with format { eligiblility_type: <unix_timestamp> }
        and compares the eligibility timestamp of each type with preconfigured
        thresholds. All applicable eligibility intervals for each
        eligibility_type are included in the result.

        For example, if the input includes an eligibility type T with a
        2-day-old timestamp and the microservice config includes possible
        eligibility intervals of 1d, 1m and 1y for eligibility type T,
        this type T will be granted eligibility values of 1m and 1y in the
        result.

        @param context: object for sharing proxy data through the current
                        request
        @param data: data carried between frontend and backend,
                     namely dict of services and timestamps of the last
                     eligible accesses of user within said service
        """
        if not self.__target_attributes:
            self.__target_attributes = self.__DEFAULT_TARGET_ATTRIBUTES

        last_seen_eligible_timestamps_dict = data.attributes.get(
            self.__eligibility_timestamps_dict_attribute, {}
        )

        if not last_seen_eligible_timestamps_dict:
            logger.info(
                "No eligibility timestamps found. Skipping this service. "
                "Attribute {self.__eligibility_timestamps_dict_attribute} might"
                " be missing in provided data"
            )
            return

        all_assurances = {}

        for (
            eligibility_type,
            details,
        ) in self.__supported_eligibility_types.items():
            provided_timestamp = last_seen_eligible_timestamps_dict.get(
                eligibility_type
            )

            if provided_timestamp:
                days_since_last_eligible_timestamp = (
                    datetime.now() - datetime.fromtimestamp(provided_timestamp)
                ).days

                assurance_prefixes = details["prefixes"]
                for period_suffix, period_duration_days in details["suffixes"].items():
                    if days_since_last_eligible_timestamp <= period_duration_days:
                        if all_assurances.get(eligibility_type) is None:
                            all_assurances[eligibility_type] = []

                        for prefix in assurance_prefixes:
                            all_assurances[eligibility_type].append(
                                f"{prefix}-{period_suffix}"
                            )

        for target_attr in self.__target_attributes:
            data.attributes.setdefault(target_attr, {}).update(all_assurances)

        return super().process(context, data)
