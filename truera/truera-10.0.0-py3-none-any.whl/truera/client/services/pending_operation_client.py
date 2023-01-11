from abc import ABC
from abc import abstractmethod
import time
from typing import Callable, Optional

from truera.client.services.mrc_client import MrcClient
from truera.client.util.absolute_progress_bar import AbsoluteProgressBars


class TimeoutExceededException(Exception):

    def __init__(self, timeout):
        self.message = f"The timeout (of {timeout}) has been exceeded."
        super().__init__(self.message)


class PendingOperationClient(ABC):
    """
    Parent class used to build clients for services that would wait for
    pending operations, e.g. AIQ or Model Test Service.
    """

    @abstractmethod
    def get_mrc_client(self) -> MrcClient:
        pass

    def _wait_till_complete(
        self,
        request_func: Callable,
        project_id: str,
        timeout: Optional[float] = None
    ):
        return self._wait_till_complete_generic(
            lambda ret: ret.pending_operations.waiting_on_operation_ids,
            request_func,
            project_id,
            timeout=timeout
        )

    def _wait_till_streaming_complete(
        self,
        pending_op_accessor: Callable,
        request_func: Callable,
        project_id: str,
        timeout: Optional[float] = None
    ):

        time_start = time.time()
        pending_operation_ids = set()
        with AbsoluteProgressBars() as progress_bars:
            while (timeout is None) or (time.time() - time_start < timeout):
                rets = [ret for ret in request_func()]
                pending_op_ids = pending_op_accessor(rets[0])
                if len(pending_op_ids) == 0:
                    progress_bars.set_percentages(
                        {
                            id: 100
                            for id in progress_bars.absolute_progress_bars
                        }
                    )
                    return rets
                for curr in pending_op_ids:
                    pending_operation_ids.add(curr)
                percentages = self.get_mrc_client().get_percentages_done(
                    project_id, sorted(list(pending_operation_ids))
                )
                progress_bars.set_percentages(percentages)
                time.sleep(1)
            raise TimeoutExceededException(timeout)

    def _wait_till_complete_generic(
        self,
        pending_op_accessor: Callable,
        request_func: Callable,
        project_id: str,
        timeout: Optional[float] = None
    ):
        time_start = time.time()
        pending_operation_ids = set()
        with AbsoluteProgressBars() as progress_bars:
            while (timeout is None) or (time.time() - time_start < timeout):
                ret = request_func()
                pending_op_ids = pending_op_accessor(ret)
                if len(pending_op_ids) == 0:
                    progress_bars.set_percentages(
                        {
                            id: 100
                            for id in progress_bars.absolute_progress_bars
                        }
                    )
                    return ret
                for curr in pending_op_ids:
                    pending_operation_ids.add(curr)
                percentages = self.get_mrc_client().get_percentages_done(
                    project_id, sorted(list(pending_operation_ids))
                )
                progress_bars.set_percentages(percentages)
                time.sleep(1)
            raise TimeoutExceededException(timeout)
