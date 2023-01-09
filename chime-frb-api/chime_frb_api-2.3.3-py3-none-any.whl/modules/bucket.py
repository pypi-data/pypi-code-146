"""CHIME/FRB Buckets API v1.0."""
import json
import warnings
from typing import Any, Optional

from chime_frb_api.core import API


class Bucket(API):
    """CHIME/FRB Backend Bucket API."""

    def __init__(
        self,
        debug: bool = False,
        base_url: str = "http://frb-vsop.chime:4357/buckets",
        authentication: bool = False,
    ):
        """CHIME/FRB Backend Bucket API.

        Args:
            debug (bool, optional): Debug mode. Defaults to False.
            base_url (_type_, optional): Base URL of the API.
                Defaults to "http://frb-vsop.chime:4357/buckets".
            authentication (bool, optional): Authentication.
                Defaults to False.
        """
        warnings.warn(
            message="\n\
            \nThe Bucket API is being deprecated and will be removed by v2022.5,\
            \nMigrate to using the Workflow API instead. If you still require the use\
            \nof low-level Bucket APIs, please move to using chimefrb.modules.buckets.\
            \n\n",
            category=DeprecationWarning,
            stacklevel=2,
        )
        API.__init__(
            self,
            debug=debug,
            default_base_urls=["http://frb-vsop.chime:4357/buckets"],
            base_url=base_url,
            authentication=authentication,
        )

    def create_bucket(self, bucket_name: str) -> Any:
        """Create a bucket on the CHIME/FRB Backend.

        Args:
            bucket_name (str): Name of the bucket

        Returns:
            Any:
        """
        payload = {"name": bucket_name}
        return self.post(url="", json=payload)

    def delete_bucket(self, bucket_name: str) -> Any:
        """Delete a bucket on the CHIME/FRB Backend.

        Args:
            bucket_name (str): Name of the bucket

        Returns:
            Any:
        """
        return self.delete(url=f"/{bucket_name}")

    def deposit(self, bucket_name: str, work: Any, priority: str) -> Any:
        """Deposit work into a bucket.

        Args:
            bucket_name (str): Name of the bucket
            work (Any): Work to be deposited
            priority (str): Priority of the work

        Returns:
            Any:
        """
        try:
            work = json.dumps(work)
        except Exception as err:
            raise (err)
        payload = {"work": [work], "priority": priority}
        return self.post(url=f"/work/{bucket_name}", json=payload)

    def withdraw(self, bucket_name: str, client: str, expiry: int) -> Any:
        """Withdraw work from a bucket.

        Args:
            bucket_name (str): Name of the bucket
            client (str): Client which is withdrawing work
            expiry (int): Expiry of the work
        """
        payload = {"client": client, "expiry": expiry}
        return json.loads(self.get(url=f"/work/{bucket_name}", json=payload))

    def conclude(
        self, bucket_name: str, work_name: str, redeposit: bool = False
    ) -> Any:
        """Conclude work in a bucket.

        Args:
            bucket_name (str): Name of the bucket
            work_name (str): Name of the work
            redeposit (bool, optional): Redeposit work. Defaults to False.
        """
        payload = {"work": work_name, "redeposit": redeposit}
        return self.post(url=f"/conclude-work/{bucket_name}", json=payload)

    def change_priority(self, bucket_name: str, work_name: str, priority: str) -> Any:
        """Change priority of work in a bucket.

        Args:
            bucket_name (str): Name of the bucket
            work_name (str): Name of the work
            priority (str): Priority of the work
        """
        payload = {"work": work_name, "priority": priority}
        return self.post(url=f"/change-priority/{bucket_name}", json=payload)

    def get_status(self, bucket_name: Optional[str] = None) -> Any:
        """Get status of a bucket.

        Args:
            bucket_name (str, optional): Name of the bucket. Defaults to None.
        """
        if bucket_name is None:
            response = self.get("")
        else:
            response = self.get(url=f"/{bucket_name}")
        return response
