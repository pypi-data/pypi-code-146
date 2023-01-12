"""CHIME/FRB Bucket API v2."""

from typing import Any, Dict, List, Optional, Union

from chime_frb_api.core import API


class Buckets(API):
    """CHIME/FRB Backend Bucket API."""

    def __init__(
        self,
        debug: bool = False,
        base_url: str = "http://localhost:8000",
        authentication: bool = False,
        **kwargs: Dict[str, Any],
    ):
        """Initialize the Buckets API.

        Args:
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            base_url (_type_, optional): The base URL of the API.
                Defaults to "http://localhost:8000".
            authentication (bool, optional): Whether to enable authentication.
                Defaults to False.
        """
        API.__init__(
            self,
            debug=debug,
            default_base_urls=[
                "http://frb-vsop.chime:8004",
                "http://localhost:8004",
                "https://frb.chimenet.ca/buckets",
            ],
            base_url=base_url,
            authentication=authentication,
            **kwargs,
        )

    def deposit(
        self, works: List[Dict[str, Any]], return_ids: bool = False
    ) -> Union[bool, List[str]]:
        """Deposit works into the buckets backend.

        Args:
            works (List[Dict[str, Any]]): The payload from the Work Object.

        Returns:
            bool: Whether the works were deposited successfully.

        Examples:
        >>> from chime_frb_api.buckets import Buckets
        >>> from chime_frb_api.tasks import Work
        >>> work = Work(pipeline="sample")
        >>> buckets.deposit([work.payload])
        True
        >>> buckets.deposit([work.payload], return_ids=True)
        ["5f9b5e1b7e5c4b5eb1b""]
        """
        if return_ids:
            return self.post(url="/work", params={"return_ids": True}, json=works)
        return self.post(url="/work", json=works)

    def withdraw(
        self,
        pipeline: str,
        event: Optional[List[int]] = None,
        site: Optional[str] = None,
        priority: Optional[int] = None,
        user: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Withdraw `queued` work from the buckets backend.

        Args:
            pipeline (str): The pipeline to withdraw from. Required.
            event (Optional[List[int]], optional): The event to withdraw from.
            site (Optional[str], optional): The site to withdraw from.
            priority (Optional[int], optional): The priority to withdraw from.
            user (Optional[str], optional): The user to withdraw from.

        Returns:
            Dict[str, Any]: The work withdrawn.
        """
        query: Dict[str, Any] = {"pipeline": pipeline}
        if site:
            query["site"] = site
        if priority:
            query["priority"] = priority
        if user:
            query["user"] = user
        if event:
            query["event"] = {"$in": event}
        response: Dict[str, Any] = self.post(url="/work/withdraw", json=query)
        return response

    def update(self, works: List[Dict[str, Any]]) -> bool:
        """Update works in the buckets backend.

        Args:
            works (List[Dict[str, Any]]): The payload from the Work Object.

        Returns:
            bool: Whether the works were updated successfully.
        """
        response: bool = self.put(url="/work", json=works)
        return response

    def delete_ids(self, ids: List[str]) -> bool:
        """Delete works from the buckets backend with the given ids.

        Args:
            ids (List[str]): The IDs of the works to delete.

        Returns:
            bool: Whether the works were deleted successfully.
        """
        return self.delete(url="/work", params={"ids": ids})

    def delete_many(
        self,
        pipeline: str,
        status: Optional[str] = None,
        events: Optional[List[int]] = None,
        force: bool = False,
    ) -> bool:
        """Delete works belonging to a pipeline from the buckets backend.

        If a status is provided, only works with that status will be deleted.
        If an event number is provided, only works with that event will be deleted.

        Args:
            pipeline (str): The pipeline to delete works from.
            status (Optional[List[str]]): The status to delete works with.
                e.g. ["queued"].
            event (Optional[List[int]]): The event to delete works with.
            force (bool, optional): Whether to force the deletion without requiring
                user confirmation. Defaults to False.

        Returns:
            bool: Whether any works were deleted.
        """
        query: Dict[str, Any] = {"pipeline": pipeline}
        if status:
            query["status"] = status
        if events:
            query["event"] = {"$in": events}
        projection = {"id": True}
        result = self.view(query, projection)
        ids: List[str] = []
        if result:
            for work in result:
                ids.append(work["id"])
        # Get user confirmation before deleting
        if ids and not force:
            # Write a warning message to the console with emojis
            print("\U0001F6A8" * 10)
            print("WARNING: This action cannot be undone.\n")
            print("You are about to delete works with parameters:")
            print(f"Bucket : {pipeline}")
            print(f"Status : {status if status else 'all'}")
            print(f"Events : {events if events else 'any'}")
            print(f"Count  : {len(ids)}\n")
            print("Are you sure? (y/n)")
            response = input()
            if response == "y":
                print("Deleting...")
                return self.delete_ids(ids)
            else:
                print("Aborting...")
                return False
        if ids and force:
            return self.delete_ids(ids)
        return False

    def status(self, pipeline: Optional[str] = None) -> Dict[str, Any]:
        """View the status of the buckets backend.

        If overall is True, the status of all pipelines will be returned.

        Args:
            pipeline (Optional[str], optional): The pipeline to return the status of.

        Returns:
            List[Dict[str, Any]]: The status of the buckets backend.
        """
        if pipeline:
            return self.get(url=f"/status/details/{pipeline}")
        else:
            return self.get(url="/status")

    def pipelines(self) -> List[str]:
        """View the current pipelines in the buckets backend.

        Returns:
            List[str]: The current pipelines.
        """
        return self.get("/status/pipelines")

    def view(
        self,
        query: Dict[str, Any],
        projection: Dict[str, bool],
        skip: int = 0,
        limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
        """View works in the buckets backend.

        Args:
            query (Dict[str, Any]): The query to filter the works with.
            projection (Dict[str, bool]): The projection to use to map the output.
            skip (int, optional): The number of works to skip. Defaults to 0.
            limit (Optional[int], optional): The number of works to limit to.
                Defaults to 100.

        Returns:
            List[Dict[str, Any]]: The works matching the query.
        """
        payload = {
            "query": query,
            "projection": projection,
            "skip": skip,
            "limit": limit,
        }
        response: List[Dict[str, Any]] = self.post("/view", json=payload)
        return response

    def audit(self) -> Dict[str, Any]:
        """Audit work buckets backend.

        The audit process retries failed work, expires any work past the
        expiration time and checks for any stale work older than 7 days.

        Returns:
            Dict[str, Any]: The audit results.
        """
        return {
            "failed": self.get("/audit/failed"),
            "expired": self.get("/audit/expired"),
            "stale": self.get("/audit/stale/7.0"),
        }
