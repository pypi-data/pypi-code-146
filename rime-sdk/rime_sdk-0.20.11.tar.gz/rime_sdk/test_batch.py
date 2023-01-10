"""Library defining the interface to a test batch object."""
import pandas as pd

from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.internal.swagger_parser import (
    parse_test_batch_result,
    parse_test_case_result,
)
from rime_sdk.internal.test_helpers import get_batch_result_response
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import ApiClient


class TestBatch:
    """An interface for a test batch in a RIME test run.

    Attributes:
        api_client: ApiClient
            The client used to query about the status of the job.
        test_run_id: str
            The string identifier for the successfully completed test run.
        test_type: str
            The unique identifer for the test type e.g. unseen_categorical.
    """

    def __init__(self, api_client: ApiClient, test_run_id: str, test_type: str) -> None:
        """Contains information about a TestBatch.

        Args:
            api_client: ApiClient
                The client used to query about the status of the job.
            test_run_id: str
                The identifier for the test run this test batch belong to.
            test_type: str
                The identifier for the test type this batch represents.
        """
        self._api_client = api_client
        self._test_run_id = test_run_id
        self._test_type = test_type

    def __repr__(self) -> str:
        """Return a string representation of the TestBatch."""
        return (
            f"TestBatch(test_run_id={self._test_run_id}, test_type={self._test_type})"
        )

    @property
    def test_run_id(self) -> str:
        """Return the test run id of the test batch."""
        return self._test_run_id

    @property
    def test_type(self) -> str:
        """Return the type of the test batch."""
        return self._test_type

    def summary(self, show_batch_metrics: bool = False) -> pd.Series:
        """Obtain the test batch summary as a Pandas Series.

        The summary contains high level information about a test batch.
        For example, the name of the test batch, the category, and the
        severity of the test batch as a whole.

        Returns:
            A Pandas Series with the following columns (and optional additional
            columns for batch-level metrics):

                1. test_run_id
                2. test_type
                3. test_name
                4. category
                5. duration_in_millis
                6. severity
                7. failing_features
                8. description
                9. summary_counts.total
                10. summary_counts.pass
                11. summary_counts.fail
                12. summary_counts.warning
                13. summary_counts.skip
        """
        res = get_batch_result_response(
            self._test_run_id, self._test_type, self._api_client,
        )
        return parse_test_batch_result(
            res.test_batch, unpack_metrics=show_batch_metrics
        )

    def get_test_cases_df(self) -> pd.DataFrame:
        """Obtain a dataframe which delinates all test cases.

        Different tests will have different columns/information.
        For example, some tests may have a column representing
        the number of failing rows.

        Returns:
            A Pandas Dataframe where each row represents a test case.
        """
        # don't forget to exhaust pages if necessary
        api = swagger_client.ResultsReaderApi(self._api_client)
        all_test_cases = []
        # Iterate through the pages of test cases and break at the last page.
        page_token = ""
        while True:
            with RESTErrorHandler():
                if page_token == "":
                    res = api.results_reader_list_test_cases(
                        list_test_cases_query_test_run_id=self._test_run_id,
                        list_test_cases_query_test_types=[self._test_type],
                        page_size=20,
                    )
                else:
                    res = api.results_reader_list_test_cases(
                        page_token=page_token, page_size=20,
                    )
            if res.test_cases:
                tc_dicts = [
                    parse_test_case_result(tc, unpack_metrics=True)
                    for tc in res.test_cases
                ]
                # Concatenate the list of test case dictionaries.
                all_test_cases += tc_dicts
            # Advance to the next page of test cases.
            page_token = res.next_page_token

            # we've reached the last page of test cases.
            if not res.has_more:
                break

        return pd.DataFrame(all_test_cases)
