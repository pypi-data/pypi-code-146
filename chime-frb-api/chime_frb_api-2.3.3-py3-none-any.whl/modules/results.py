"""CHIME/FRB workflow Results API."""

from typing import Any, Dict, List, Optional

from chime_frb_api.core import API


class Results(API):
    """CHIME/FRB Backend workflow Results API."""

    def __init__(
        self,
        debug: bool = False,
        base_url: str = "http://localhost:8005",
        authentication: bool = False,
        **kwargs: Dict[str, Any],
    ):
        """Initialize the workflow Results API.

        Args:
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            base_url (str, optional): The base URL of the API.
                Defaults to "http://localhost:8005".
            authentication (bool, optional): Whether to enable authentication.
                Defaults to False.
        """
        API.__init__(
            self,
            debug=debug,
            default_base_urls=["http://frb-vsop.chime:8005", "http://localhost:8005"],
            base_url=base_url,
            authentication=authentication,
            **kwargs,
        )

    def deposit(self, works: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Deposit works into the results backend.

        Args:
            works (List[Dict[str, Any]]): A list of payloads from Work Objects.
        Note:
            This method is not intended to be called directly by end users.

        Returns:
            Dict[str, bool]: Dictionary of deposit results for each pipeline.

        Examples:
        >>> from chime_frb_api.results import Results
        >>> from chime_frb_api.tasks import Work
        >>> work = Work.fetch(pipeline="sample")
        >>> results = Results()
        >>> status = results.deposit([work.payload])
        """
        for work in works:
            assert work["status"] in [
                "success",
                "failure",
            ], "Work status must be 'success' or 'failure'"
        return self.post(url="/results", json=works)

    def update(self, works: List[Dict[str, Any]]) -> bool:
        """Update works in the results backend.

        Args:
            works (List[Dict[str, Any]]): A list of payloads from Work Objects.
        Note:
            The results need to exist before they can be updated.

        Returns:
            bool: Whether the works were updated successfully.
        """
        response: bool = self.put(url="/results", json=works)
        return response

    def delete_ids(self, pipeline: str, ids: List[str]) -> bool:
        """Delete results from the results backend with the given ids.

        Args:
            pipeline (str): Name of pipeline that the IDs are from.
            ids (List[str]): The IDs of the works to delete.

        Returns:
            bool: Whether the results were deleted successfully.
        """
        return self.delete(url="/results", params={pipeline: ids})

    def view(
        self,
        pipeline: str,
        query: Dict[str, Any],
        projection: Dict[str, bool],
        skip: int = 0,
        limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
        """View works in the workflow results backend.

        Args:
            pipeline (str): Name of pipeline to query results.
            query (Dict[str, Any]): The query to filter the results with.
            projection (Dict[str, bool]): The projection to use to map the output.
            skip (int, optional): The number of works to skip. Defaults to 0.
            limit (Optional[int], optional): The number of works to limit to.
                Defaults to 100.

        Returns:
            List[Dict[str, Any]]: The works matching the query.
        """
        query["pipeline"] = pipeline
        payload = {
            "query": query,
            "projection": projection,
            "skip": skip,
            "limit": limit,
        }
        response: List[Dict[str, Any]] = self.post("/view", json=payload)
        return response

    def count(
        self,
        pipeline: str,
        query: Dict[str, Any],
    ) -> int:
        """Retrieve the number of results filtered by the query parameters.

        Args:
            pipeline (str): Name of pipeline to query results.
            query (Dict[str, Any]): The query to filter the results with.

        Returns:
            int: The number of results that match the query.
        """
        query["pipeline"] = pipeline
        payload = {
            "query": query,
        }
        response: int = self.post("/view/count", json=payload)
        return response

    def status(self) -> Dict[str, int]:
        """Retrieve the overall status of the results backend.

        Returns:
            Dict[str, int]: The status of the results backend.
        """
        response: Dict[str, int] = self.get("/status")
        return response
