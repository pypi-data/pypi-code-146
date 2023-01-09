"""Useful functions for concurrency in tests.

In particular, running a modeller and multiple local workers.
"""
import asyncio
from asyncio import Task
from concurrent.futures import ThreadPoolExecutor
import logging
import threading
from typing import Any, Coroutine, List, Literal, Optional, TypeVar, Union

from bitfount import _Modeller
from bitfount.federated.transport.base_transport import _run_func_and_listen_to_mailbox
from bitfount.federated.worker import _Worker
from bitfount.utils.concurrency_utils import await_threading_event

_logger = logging.getLogger(__name__)

_R = TypeVar("_R")


def _modeller_run(
    modeller: _Modeller, pod_identifiers: List[str], stop: threading.Event
) -> Union[Literal[False], Optional[Any]]:
    """Run _Modeller.run_async() synchronously.

    Designed to be the target of a thread.
    """
    result = asyncio.run(_async_modeller_run(modeller, pod_identifiers, stop))
    _logger.info("Finished modeller_run")
    return result


async def _async_modeller_run(
    modeller: _Modeller, pod_identifiers: List[str], stop: threading.Event
) -> Union[Literal[False], Optional[Any]]:
    """Run _Modeller.run_async() and monitor for stop event."""
    result = await _run_coro_with_stop(
        coro=modeller.run_async(pod_identifiers, True),
        coro_task_name="modeller_run_async_task",
        stop_event=stop,
        stop_event_task_name="modeller_run_stop",
    )

    _logger.info(f"modeller_run_async_task done, result: {result}")
    return result


def _worker_run(worker: _Worker, stop: threading.Event) -> None:
    """Run _Worker.run() synchronously.

    Designed to be the target of a thread.
    """
    asyncio.run(_async_worker_run(worker, stop))
    _logger.info(f"Finished worker_run for worker {worker.pod_identifier}")


async def _async_worker_run(worker: _Worker, stop: threading.Event) -> None:
    """Run _Worker.run() and monitor for stop event.

    Also handles the mailbox listening.
    """
    await _run_coro_with_stop(
        coro=_run_func_and_listen_to_mailbox(worker.run(), worker.mailbox),
        coro_task_name=f"worker_{worker.pod_identifier}_run_async_task",
        stop_event=stop,
        stop_event_task_name=f"worker_{worker.pod_identifier}_run_stop",
    )
    _logger.info(f"worker_{worker.pod_identifier}_run_async_task done")


async def _run_coro_with_stop(
    coro: Coroutine[Any, Any, _R],
    coro_task_name: str,
    stop_event: threading.Event,
    stop_event_task_name: str,
) -> _R:
    """Run a coroutine whilst monitoring for a thread-safe stop event."""
    # Create explicit tasks so we can target them later.
    run_task = asyncio.create_task(
        coro,
        name=coro_task_name,
    )
    stop_task = asyncio.create_task(
        await_threading_event(stop_event, stop_event_task_name),
        name=stop_event_task_name,
    )

    try:
        # Run until either run_task is complete or stop event is set.
        aws: List[Task] = [run_task, stop_task]
        await asyncio.wait(aws, return_when=asyncio.FIRST_COMPLETED)
    except BaseException as e:
        _logger.exception(e)
        raise e
    finally:
        # Find out which task is complete and cancel the other one as needed
        if not run_task.done():
            _logger.error(f"{run_task.get_name()} did not finish, cancelling")
            run_task.cancel()
            try:
                await run_task
            except asyncio.CancelledError:
                pass

        if not stop_task.done():
            _logger.warning(
                f"{stop_task.get_name()} did not finish, cancelling but not awaiting"
            )
            stop_task.cancel()

    return run_task.result()


async def run_local_modeller_and_workers(
    modeller: _Modeller,
    workers: List[_Worker],
) -> Union[Literal[False], Optional[Any]]:
    """Run a pre-configured modeller and workers to task completion.

    Args:
        modeller: The modeller to run.
        workers: The list of workers to run.

    Returns:
        The results of the modeller execution.
    """
    stop_event = threading.Event()
    with ThreadPoolExecutor(max_workers=(1 + len(workers))) as pool:
        try:
            # Create futures for the modeller and workers running.
            main_loop = asyncio.get_running_loop()
            modeller_fut = main_loop.run_in_executor(
                pool,
                _modeller_run,
                modeller,
                [worker.mailbox.pod_identifier for worker in workers],
                stop_event,
            )
            worker_futs = [
                main_loop.run_in_executor(pool, _worker_run, worker, stop_event)
                for worker in workers
            ]

            # Execute until all are done or an exception is raised.
            try:
                modeller_results, *_ = await asyncio.gather(modeller_fut, *worker_futs)
            except BaseException as e:
                _logger.exception(e)

                # Tell other tasks to stop execution within their own threads
                _logger.error("Setting stop_event")
                stop_event.set()

                # Cancel tasks (if already executing won't stop execution,
                # stop_event does that).
                # Can't use gather_task.cancel() as that is already "done" by this point
                to_await: List[asyncio.Future] = []

                # Cancel modeller
                if not modeller_fut.done():
                    _logger.error(
                        f"Cancelling outstanding modeller future {modeller_fut=}"
                    )
                    modeller_fut.cancel()
                    to_await.append(modeller_fut)
                else:
                    _logger.info(f"Modeller task already finished {modeller_fut=}")

                # Cancel workers
                for fut in worker_futs:
                    if not fut.done():
                        _logger.error(f"Cancelling outstanding worker future {fut=}")
                        fut.cancel()
                        to_await.append(fut)
                    else:
                        _logger.info(f"Worker future already finished {fut=}")

                # Await those cancelled tasks
                for fut in to_await:
                    try:
                        _logger.error(f"Waiting for cancelled future to finish {fut=}")
                        await fut
                    except asyncio.CancelledError:
                        pass

                _logger.error("All tasks cancelled")
                raise e
        finally:
            # Guarantee it is set, even if not exceptions
            if not stop_event.is_set():
                _logger.info("Setting stop_event")
                stop_event.set()

        _logger.debug("End of thread pool execution")

    _logger.debug("Fully out of thread pool execution")

    return modeller_results
