from collections import namedtuple
from datetime import datetime
from decimal import Decimal
import json
import logging
from typing import NamedTuple

import arrow

from . import Client, ClientError, retry, TransientServerError

logger = logging.getLogger(__name__)

decimal_metrics = ["actual_pub_payout", "dooh_impmultiply"]


class EntrySet(NamedTuple):
    timestamp: datetime
    entries: list


class SlicerClient(Client):
    """HTTP client for the u-Slicer API.

    https://confluence.iponweb.net/display/UPLATFORMKB/API

    >>> from rbx.clients.uslicer import SlicerClient
    >>> client = SlicerClient(token='eyJhbGciOiJFU...')

    """

    TIME_FORMAT = "YYYY-MM-DD"
    DEFAULT_TIMEOUT = 60
    ENDPOINT = "https://uslicer.iponweb.com/API/v2/query"

    def __init__(self, token, project_name="rockabox", slicer_name="Traffic"):
        super().__init__()
        self.token = token
        self.project_name = project_name
        self.slicer_name = slicer_name

        self.breakdowns = []
        self.metrics = []

    @property
    def entry(self):
        assert (
            self.breakdowns and self.metrics
        ), "An entry only exists after a query has been executed"
        return namedtuple(
            "Entry", map(lambda x: x.split(".")[-1], self.breakdowns + self.metrics)
        )

    def fetch(self, breakdowns, metrics, start_date, end_date, filters=None):
        """fetch u-Slicer metrics in hourly batches.

        The method uses the same signature as the `query()` method, but instead returns an
        iterator, which yields hourly results.

        Unlike `query()`, however, this methods allows fetching data with more precise start and
        end dates, using hours as well as days.

        Note that both the start and end dates are rounded to the previous hour. As uSlicer does
        not handle that level of precision, this is made cleared that way. The `timestamp` datetime
        attribute of each iteration will use that rounded date.
        """
        start_date = arrow.get(start_date).floor("hour")
        end_date = arrow.get(end_date).floor("hour")
        filters = filters or []
        for r in arrow.Arrow.range("hour", arrow.get(start_date), arrow.get(end_date)):
            results = self.query(
                breakdowns,
                metrics,
                start_date=r.format(self.TIME_FORMAT),
                end_date=r.format(self.TIME_FORMAT),
                filters=filters + [("hour", "equals", [r.format("H")])],
            )

            yield EntrySet(timestamp=r.datetime, entries=results)

    @retry.Retry(deadline=300.0)
    def query(
        self,
        breakdowns,
        metrics,
        start_date,
        end_date,
        filters=None,
        none_default="N/A",
    ):
        """Fetch u-Slicer metrics.

        The metrics are returned for the given date range. The start and end dates are given as
        datetime objects.

        The optional `filters` argument takes a LIST of filter tuples.
        e.g.:
        >>> filters = [(Breakdown.CAMPAIGN, Operator.EQUALS, [123234453])]

        The values are returned as a list of Entry objects.
        """
        self.breakdowns = breakdowns
        self.metrics = metrics

        params = {
            "project_name": self.project_name,
            "slicer_name": self.slicer_name,
            "token": self.token,
            "data_fields": metrics,
            "end_date": arrow.get(end_date).format(self.TIME_FORMAT),
            "limit": -1,
            "split_by": breakdowns,
            "start_date": arrow.get(start_date).format(self.TIME_FORMAT),
            "timezone": 0,
        }

        # Resolve each filter tuple in the filters list.
        _filters = []
        if filters:
            for breakdown, operator, value in filters:
                _filters.append({"name": breakdown, "match": operator, "value": value})

        if _filters:
            params["filters"] = _filters

        logger.debug(f"Query params: {params}")
        try:
            response = self.request("post", self.ENDPOINT, data=params)
        except ClientError as exc:
            try:
                message = json.loads(str(exc))
            except json.decoder.JSONDecodeError as e:
                raise exc from e
            else:
                if message.get("status") == "internal_error":
                    raise TransientServerError(
                        exc,
                        details=exc.details,
                        status_code=exc.status_code,
                        url=exc.url,
                    )
                else:
                    raise

        results = []

        for row in response["rows"]:

            # Annoyingly Iponweb have decided to call the Panel ID field 'supply.panel_id',
            # which is not namedtuple-friendly. So here we apply that logic to all fields in an
            # attempt to be future-proof, namely to remove all dot prefixes.
            # Plus, empty/null breakdowns get replaced with custom value (which defaults to 'N/A').
            fields = {}
            for i, breakdown in enumerate(breakdowns):
                fields[breakdown.split(".")[-1]] = row["name"][i] or none_default

            fields.update(
                dict(
                    [
                        (
                            metric["name"],
                            Decimal(str(metric["value"]))
                            if metric["name"] in decimal_metrics
                            else metric["value"],
                        )
                        for metric in row["data"]
                    ]
                )
            )

            results.append(self.entry(**fields))

        logger.debug(f"Found {len(results)} entries.")

        return results
