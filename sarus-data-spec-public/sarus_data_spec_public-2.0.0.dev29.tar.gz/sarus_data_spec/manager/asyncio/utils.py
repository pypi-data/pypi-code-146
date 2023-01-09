import asyncio
import threading
import typing as t

import sarus_data_spec.typing as st

T = t.TypeVar("T")
MAX_QUEUE_SIZE = 10


# Custom Thread Class
class ThreadWithException(threading.Thread):
    """Custom class to catch errors occuring
    in a thread and passing them to the main
    one
    """

    def run(self) -> None:
        # Variable that stores the exception, if raised
        self.exc = None
        try:
            super().run()
        except BaseException as exception:
            self.exc = exception

    def join(self, timeout: t.Optional[float] = None) -> None:
        threading.Thread.join(self)
        # Since join() returns in caller thread
        # we re-raise the caught exception
        # if any was caught
        if self.exc:
            raise self.exc


def sync(coro: t.Coroutine) -> t.Any:
    """This runs an async function synchronously,
    even within an already runnning event loop,
    despite the apparent impossibility
    to nest loops within the same thread"""
    result = None
    # Define the thread job

    def sync_job() -> t.Any:
        nonlocal result
        result = asyncio.run(coro)

    # Run the thread
    sync_job_thread = ThreadWithException(target=sync_job)
    sync_job_thread.start()
    sync_job_thread.join()
    return result


def sync_iterator(
    async_iterator_coro: t.Coroutine,
) -> st.ContextManagerIterator[T]:
    """This methods returns an iterator from an async iterator coroutine.

    To allow nesting calls to asyncio, the async coroutine is run in another
    thread. When the generator is consumed, the thread runs. In situations
    where the generator might not be consumed completely, the iterator
    can be run as a context manager: when exiting, it is stopped and
    the thread closed.

    It is build on two sync functions: one that adds
    batches on a queue and one that takes them from the queue. They both
    share a newly created event loop on which to run async methods and
    the queue object in which adding/taking the batches.

    The producing method (sync_producer job) is run on a new thread and
    executes the async_produce method.

    The method that reads the batches from the queue (sync_consumer) executes
    async_consume (that returns one batch of data) and yields the batch.
    It stops when the first receieved batch is None.
    """
    # The loop used in the thread and shared among functions
    loop = asyncio.new_event_loop()
    # The queue to add the iterator elements
    queue = None

    # A signal to specify that the iterator should be stopped
    stop_iteration = False

    # -------Now, we define all the methods we need-------------

    def sync_producer_job() -> None:
        """Methods that launches the
        execution of async_iterator coroutine"""
        nonlocal loop
        nonlocal queue
        asyncio.set_event_loop(loop)
        queue = asyncio.Queue(MAX_QUEUE_SIZE)
        loop.run_until_complete(async_produce())

    async def async_produce() -> None:
        """Method that puts batches in the queue asynchronously.
        There are three steps:
        - first the iterator per se is awaited. A special token () is
        added to the queue to signal it. We do this because the sync
        generator should be returned in the end after the async iterator
        is ready.
        - then each batch is retrieved and added to the queue
        - when the batches are finished/ an exception occurs a token None
         is added as a signal that the iteration is finished
        """
        nonlocal queue
        nonlocal stop_iteration
        assert queue is not None
        try:
            async_iterator = await async_iterator_coro
            # we add a first element to signal that
            # the async_iterator is ready
            await queue.put(())
        except Exception as exception:
            # we need to add it also here
            # because the consumer removes it all
            # the time
            await queue.put(())
            # None signals the end of the queue
            # for the consumer
            await queue.put(None)
            await queue.join()
            raise exception
        try:
            batch = await async_iterator.__anext__()
        except Exception as exception:
            if isinstance(exception, StopAsyncIteration):
                # None signals the end of the queue
                # for the consumer
                batch = None
            else:
                raise exception
        else:
            await queue.put(batch)
        while batch is not None and not stop_iteration:
            try:
                batch = await async_iterator.__anext__()
            except Exception as exception:
                batch = None
                if isinstance(exception, StopAsyncIteration):
                    pass
                else:
                    # this is needed
                    # to end the consumer in case
                    # of exception
                    await queue.put(None)
                    await queue.join()
                    raise exception
            else:
                await queue.put(batch)
        await queue.put(None)
        await queue.join()

    def sync_consumer() -> t.Iterator[T]:
        """Generator of batches"""
        nonlocal loop
        nonlocal sync_job_thread  # type:ignore
        nonlocal stop_iteration

        value = asyncio.run_coroutine_threadsafe(
            async_consume(), loop
        ).result()
        while value is not None and not stop_iteration:
            yield value
            value = asyncio.run_coroutine_threadsafe(
                async_consume(), loop
            ).result()
        sync_job_thread.join()

    async def async_consume() -> T:
        """Async method that retrieves one
        element from the queue"""
        nonlocal queue
        assert queue is not None
        nonlocal stop_iteration

        if stop_iteration:
            # event signal that allows the async
            # producer to stop and so the thread
            # to be closed
            queue._unfinished_tasks = 0
            queue._finished.set()
            return None

        value = await queue.get()
        queue.task_done()
        return value

    # --------Execution of the different methods------------

    # Run the thread with the producer method
    sync_job_thread = ThreadWithException(target=sync_producer_job)
    sync_job_thread.start()
    # Run the consumer
    generator = sync_consumer()

    # we make sure the async iterator task is finished
    # by iterating on the first value, removing so
    # the special token ()
    next(generator)

    class ContextManagerIterator:
        """Class that that allows either to
        iterate directly on the generator if iter
        is called or if called as a context manager
        (with ...) it allows to always close
        the thread opened with async_produce if"""

        def __enter__(self) -> t.Iterator[T]:
            return generator

        def __next__(self) -> T:
            return next(generator)

        def __iter__(self) -> 'ContextManagerIterator':
            return self

        def __exit__(
            self, exc_type: t.Any, exc_val: t.Any, exc_tb: t.Any
        ) -> None:
            nonlocal stop_iteration
            stop_iteration = True
            try:
                next(generator)  # if the generator
                # is not finished this allows to close
                # the thread of async_produce
            except StopIteration:
                pass

    return ContextManagerIterator()


async def async_iter(data_list: t.Collection[T]) -> t.AsyncIterator[T]:
    """Convert a collection into an AsyncIterator."""
    for data in data_list:
        yield data


async def decoupled_async_iter(
    source: t.AsyncIterator[T], buffer_size: int = 1
) -> t.AsyncIterator[T]:
    """Create a consumer/producer pattern using an asyncio.Queue."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)

    async def producer() -> None:
        async for x in source:
            await queue.put(x)
        await queue.put(None)  # producer finished

    # Launch the iteration of source iterator
    loop = asyncio.get_running_loop()
    loop.create_task(producer())

    while True:
        x = await queue.get()
        if x is None:
            queue.task_done()
            break
        queue.task_done()
        yield x
