from threading import Lock
from time import sleep, time
from math import ceil, inf
from os import environ

from psutil import Process, cpu_count, cpu_times

from .cgroups import get_cgroups_cpu_quota

# How often to poll the CPU, compared to the moving-average of the job-start-interval
CPU_IDLE_POLL_DIVISOR = 20

# Polling the cpu-idle more often than this is bound to give noisy results
# If your application consumes jobs more often than this, pothead probably is not for you
CPU_IDLE_POLL_MIN_INTERVAL = 0.050
CPU_IDLE_POLL_MAX_INTERVAL = 2

# The worker will ignore available idle CPU until it is using at least this much CPU itself
# Useful for shared environments like in Kubernetes where neighbor pods might use your `cpu.request`
# oppotunistically, until you use it yourself
CPU_PROMISED = int(environ.get("POTHEAD_CPU_PROMISED", 0))

# Jobs will still be clamped to idle CPU, but we want SOME kind of upper bound on concurrency, to avoid
# temporary I/O blockage causing ridiculous amounts of work
DEFAULT_MAX_CONCURRENT_MULTIPLIER = 2

__all__ = ["wait_for_idle_cpus"]


class MovingAverage:
    def __init__(self, init=0, inertia=0.6):
        self.value = init
        self.speed = 1 - inertia
        self.inertia = inertia

    def update(self, value):
        self.value = (self.value * self.inertia) + (value * self.speed)
        return self.value


class Worker:
    def __init__(self, cpu_reservation_amount, keep_cpu_reservation):
        self.cpu_reservation_amount = cpu_reservation_amount
        self.keep_cpu_reservation = keep_cpu_reservation
        self.on_done = None

    def reset_cpu_reservation(self, new_cpu_amount=0):
        # Note: we rely on the GIL/atomicity of Python bytecode execution
        # here, since this value will be changed from the handler thread,
        # but read (via `reserved_cpu_amount()`) in the `wait_for_slot()`
        # thread.
        self.cpu_reservation_amount = new_cpu_amount
        # Note: we do not call on_done() here, even if the amount would be 0
        # since that would remove a live worker from the list, which would give
        # the wrong worker count

    # Worker callback implementation
    def request_received(self, environ):
        environ["RESET_CPU_RESERVATION"] = self.reset_cpu_reservation
        if not self.keep_cpu_reservation:
            self.reset_cpu_reservation(0)

    # Worker callback implementation
    def done(self):
        self.on_done(self)


class WorkerList:
    def __init__(self):
        self.workers = set()
        self.lock = Lock()

    def add_worker(self, worker):
        with self.lock:
            worker.on_done = lambda w: self.remove_worker(w)
            self.workers.add(worker)
        return worker

    def remove_worker(self, worker):
        with self.lock:
            self.workers.remove(worker)

    def __len__(self):
        with self.lock:
            return len(self.workers)

    def reserved_cpu_amount(self):
        with self.lock:
            return sum([w.cpu_reservation_amount for w in self.workers])


"""Timed measurement on an incrementing counter

Reads the counter, divides with time passed since last reading, and smooths the value using a moving average
"""


class InertialTimeDerivate:
    def __init__(self, func, initial, inertia):
        self.func = func
        self.last_value = self.func()
        self.last_check = time()
        self.inertial_value = MovingAverage(initial, inertia)

    def update(self):
        new_value = self.func()
        this_check = time()
        elapsed = this_check - self.last_check
        delta = new_value - self.last_value
        self.last_check = this_check
        self.last_value = new_value
        return self.inertial_value.update(delta / elapsed)


def wait_for_idle_cpus(
    required, *, max_concurrent=None, inertia=0.7, keep_cpu_reservation=False
):
    """CPU-gated wait_for_slot implementation

    Creates a wait_for_slot-callable that will let through at least one concurrent job, and additional jobs as
    long as `required` cpu:s are idle. It is cgroup-aware, and will not allow current process and subprocesses to
    consume more CPU than configured cgroup-limit.

    When a worker is spawned, but before it has received its job request, it will have the CPU amount
    specified in the `required` parameter artificially reserved for it. The `keep_cpu_reservation`
    parameter can be used for jobs that when started don't immediately use the full amount of CPU that
    they will do eventually. In order to avoid spawning lots of such jobs in a short time period before
    CPU usage has settled, the artifical CPU reservation can be kept by setting `keep_cpu_reservation`
    to True. When doing this, the job should at some later point during its request processing reset the
    CPU reservation by calling the function stored under the "RESET_CPU_RESERVATION" key in the WSGI
    request environment, like so:

        http_request.environ["RESET_CPU_RESERVATION"](new_cpu_amount)

    The function may be called several times during the request processing, but the last call should
    normally set the amount to 0.
    """
    worker_list = WorkerList()
    cpu_wait_time = MovingAverage(1, 0.7)

    process = Process()

    def cpu_used_in_process():
        times = process.cpu_times()
        return times.user + times.system + times.children_user + times.children_system

    cpu_quota = get_cgroups_cpu_quota()
    if cpu_quota < inf:
        if not max_concurrent:
            max_concurrent = ceil(
                cpu_quota * DEFAULT_MAX_CONCURRENT_MULTIPLIER / required
            )

        # Precalculate the quota with headroom for a new job
        cpu_quota -= required
    else:
        if not max_concurrent:
            max_concurrent = ceil(
                cpu_count() * DEFAULT_MAX_CONCURRENT_MULTIPLIER / required
            )

    def cpu_is_available(idle, cpu_used):
        reserved = worker_list.reserved_cpu_amount()
        cpu_used += reserved

        if cpu_used < CPU_PROMISED:
            return True

        if idle - reserved < required:
            return False

        return cpu_used <= cpu_quota

    def wait_for_slot(halt):
        start_time = time()

        idle = InertialTimeDerivate(lambda: cpu_times().idle, 0, inertia)
        cpu_used = InertialTimeDerivate(cpu_used_in_process, cpu_count(), inertia)

        cpu_poll_interval = max(
            CPU_IDLE_POLL_MIN_INTERVAL,
            min(
                cpu_wait_time.value / CPU_IDLE_POLL_DIVISOR, CPU_IDLE_POLL_MAX_INTERVAL
            ),
        )
        while len(worker_list) and not halt():
            idle_deriv = idle.update()
            cpu_used_deriv = cpu_used.update()
            if len(worker_list) < max_concurrent and cpu_is_available(
                idle_deriv, cpu_used_deriv
            ):
                break

            sleep(cpu_poll_interval)

        cpu_wait_time.update(time() - start_time)

        return worker_list.add_worker(Worker(required, keep_cpu_reservation))

    return wait_for_slot
