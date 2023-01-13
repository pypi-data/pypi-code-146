#!/usr/bin/env python3

from http import HTTPStatus
from logging import getLogger
from signal import SIGTERM, signal
from socket import (
    AF_INET,
    IPPROTO_TCP,
    SHUT_RDWR,
    SO_KEEPALIVE,
    SOCK_STREAM,
    SOL_SOCKET,
    TCP_KEEPCNT,
    TCP_KEEPIDLE,
    TCP_KEEPINTVL,
    getaddrinfo,
    socket,
)
from threading import Thread, Timer
from time import monotonic, sleep
from typing import Dict, Optional, Set
from uuid import uuid4
from wsgiref import simple_server

from werkzeug.serving import WSGIRequestHandler

from .gating import wait_for_idle_cpus
from .oob_response import OutOfBandResponder
from .resource_balancer import BoundedResourceBalancer, ResourceLoan
from .util import ObjectProxy, ThreadsTracker

LOGGER = getLogger("pothead.worker")
BROKER_CONNECT_RETRY_INTERVAL = 2


class DeferrableCleanup:
    def __init__(self, f):
        self.f = f

    def assume(self):
        f = self.f
        self.f = None
        return f

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        if self.f:
            self.f()


class Handler(WSGIRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(
        self, socket, address, server, cb_request_received, cb_processing_done
    ):
        self.cb_request_received = cb_request_received
        self.env = None
        self.uuid = uuid4()
        self.request_received_at = None

        with DeferrableCleanup(cb_processing_done) as c:
            if isinstance(server.app, OutOfBandResponder):
                app = server.app
                server = ObjectProxy(server)
                server.app = lambda environ, start_response: app(
                    environ, start_response, c.assume
                )

            super().__init__(socket, address, server)

    def handle_one_request(self):
        try:
            # Handler may be used for several requests, so we must reset
            # environment overrides each time
            self.env = None
            super().handle_one_request()
        finally:
            self.close_connection = True

    def make_environ(self):
        environ = super().make_environ()

        if self.cb_request_received:
            self.cb_request_received(environ)

        return environ

    def parse_request(self):
        success = super().parse_request()

        # This socket shall no longer be fast-closed on SIGTERM
        socket = self.request
        self.server.sockets_waiting_for_request.remove(socket)

        return success

    def log_message(self, format, *args):
        LOGGER.info("[%s] " + format, self.uuid, *args)

    def log_request(self, code="-", size="-"):
        self.request_received_at = monotonic()
        if isinstance(code, HTTPStatus):
            code = code.value
        LOGGER.info(
            '[%s] "%s" %s %s', self.uuid, self.requestline, str(code), str(size)
        )

    def log_error(self, format, *args):
        LOGGER.error("[%s] " + format, self.uuid, *args)

    def log_elapsed(self):
        LOGGER.info(
            "[%s] Elapsed: %s" % (self.uuid, monotonic() - self.request_received_at)
        )


class LoadBalancer:
    REFRESH_INTERVAL = 5

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._balancer = BoundedResourceBalancer(1)
        self.refresh()

    def acquire_addr(self) -> ResourceLoan:
        return self._balancer.acquire()

    def refresh(self):
        try:
            results = getaddrinfo(self.host, self.port, type=SOCK_STREAM)
            hosts = (sockaddr for _f, _t, _p, _c, sockaddr in results)
            self._balancer.provision(hosts)
        except BaseException:
            LOGGER.exception(
                "Failed to refresh endpoints for %s:%d", self.host, self.port
            )
        t = Timer(self.REFRESH_INTERVAL, self.refresh)
        t.daemon = True
        t.start()


class Server:
    ssl_context = None
    multithread = False
    multiprocess = False
    passthrough_errors = False
    shutdown_signal = False
    running = True

    def __init__(
        self,
        addr,
        app,
        *,
        load_balancer=LoadBalancer,
        redirect_port: Optional[int] = None,
        oob_cleanup_interval_seconds: Optional[float] = None,
        oob_item_expiry_seconds: Optional[float] = None,
    ):
        (host, port) = addr
        # Set up base environment
        env: Dict[str, str] = {}
        env["SERVER_NAME"] = host
        env["GATEWAY_INTERFACE"] = "HTTP/1.1"
        env["SERVER_PORT"] = port
        env["REMOTE_HOST"] = ""
        env["CONTENT_LENGTH"] = ""
        env["SCRIPT_NAME"] = ""
        self.base_environ = env

        self.broker_balancer = load_balancer(host, port)
        self.sockets_waiting_for_request: Set[socket] = set()
        self.real_app = app
        self.worker_tracker = ThreadsTracker()
        self.app = (
            OutOfBandResponder(
                app,
                redirect_port,
                oob_cleanup_interval_seconds,
                oob_item_expiry_seconds,
            )
            if redirect_port is not None
            else app
        )

    def worker(self):
        while self.running:
            with self.worker_tracker, self.broker_balancer.acquire_addr() as addr:
                self._fetch_and_run_one_job(addr)

    def _fetch_and_run_one_job(
        self, addr, cb_request_received=None, cb_processing_done=lambda: None
    ):
        with socket(AF_INET, SOCK_STREAM) as s:
            self.sockets_waiting_for_request.add(s)
            try:
                s.connect(addr)
                self.server_address = s.getsockname()

                s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                s.setsockopt(IPPROTO_TCP, TCP_KEEPIDLE, 1)
                s.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, 2)
                s.setsockopt(IPPROTO_TCP, TCP_KEEPCNT, 3)
            except Exception as e:
                LOGGER.error("Couldn't connect to broker: %r", e)
                cb_processing_done()
                sleep(BROKER_CONNECT_RETRY_INTERVAL)
                return

            try:
                h = Handler(s, addr, self, cb_request_received, cb_processing_done)
                if h.request_received_at:
                    h.log_elapsed()
            except BaseException:
                LOGGER.exception("In WSGI request handling")
                sleep(1)
                return

    def get_app(self):
        return self.app

    def shutdown(self):
        LOGGER.info("Shutting down workers...")
        self.running = False
        for s in list(self.sockets_waiting_for_request):
            try:
                s.shutdown(SHUT_RDWR)
                s.close()
            except OSError:
                pass

        self.worker_tracker.drain()

        if isinstance(self.app, OutOfBandResponder):
            self.app.shutdown()
        LOGGER.info("Worker shutdown completed")

    def poll_loop(self):
        """Uses app.wait_for_slot() spawn new workers dynamically. This is useful, for example to wait for
        enough CPU, memory, or disk space, to start next job.

        `wait_for_slot` is expected to block until it's time to poll for a new job. It is given a function
        `halt` which it should poll intermittently to check if this worker is undergoing `shutdown()`.

        It may return an object, if so `obj.request_received(environ)` will be called when a request is
        received and `obj.done()` when either the request is received, or if polling failed in which case
        `request_received()` was never called.

        See pothead.gating for some ready-made `wait_for_slot` implementations"""

        while self.running:
            callbacks = self.real_app.wait_for_slot(lambda: not self.running)
            if not self.running:
                break

            # This will block as long as we are waiting for requests from all broker-instances
            broker_instance_lease = self.broker_balancer.acquire_addr()
            if not self.running:
                break

            Thread(
                target=self._run_one_poll, args=(broker_instance_lease, callbacks)
            ).start()

    def _run_one_poll(self, broker_instance_lease: ResourceLoan, callbacks):
        def request_received(environ):
            broker_instance_lease.release()
            getattr(callbacks, "request_received", lambda _: None)(environ)

        with self.worker_tracker, broker_instance_lease as addr:
            self._fetch_and_run_one_job(
                addr, request_received, getattr(callbacks, "done", lambda: None)
            )

    def log(self, type, msg, *args, **kwargs):
        getattr(LOGGER, type)(msg.rstrip(), *args, **kwargs)


def install_term_handler(f):
    previous = []

    def on_term(_signal, _stack):
        Thread(target=f).start()
        for p in previous:
            p()

    p = signal(SIGTERM, on_term)
    if p:
        previous.append(p)


demo_app = simple_server.demo_app
demo_app.wait_for_slot = wait_for_idle_cpus(3)


if __name__ == "__main__":
    from argparse import ArgumentParser
    from importlib import import_module
    from logging import INFO, basicConfig
    from os import environ
    from sys import path

    path.insert(0, ".")

    def address(str):
        (host, port) = str.rsplit(":", 1)
        return (host, int(port))

    def func(str):
        (module, symbol) = str.rsplit(":", 1)
        module = import_module(module)
        return getattr(module, symbol)

    DEFAULT_WORKERS = int(environ.get("POTHEAD_WORKERS", 1))

    parser = ArgumentParser(description="Run WSGI app in sequential `worker` mode")
    parser.add_argument(
        "--connect",
        default="localhost:4040",
        type=address,
        help="Load Balancer Hub to connect to [host:port]",
    )
    parser.add_argument(
        "--redirect-response",
        default=None,
        help="When streaming successful responses, first redirect client to worker at [port]",
    )
    job_control_group = parser.add_mutually_exclusive_group()
    job_control_group.add_argument(
        "--workers",
        default=DEFAULT_WORKERS,
        type=int,
        help="Number of worker Processes",
    )
    job_control_group.add_argument(
        "--poll-jobs",
        action="store_true",
        help="Use `app.wait_for_slot` to determine when to pull new jobs",
    )

    parser.add_argument(
        "app",
        nargs="?",
        default="pothead.worker:demo_app",
        type=func,
        help="The WSGI request handler to handle requests",
    )
    args = parser.parse_args()
    basicConfig(level=INFO)

    LOGGER.info("Initializing server for app %s", args.app)

    server = Server(args.connect, args.app, redirect_port=args.redirect_response)

    install_term_handler(server.shutdown)

    if args.poll_jobs:
        LOGGER.info(
            "Starting up job-polling dynamic workers connecting to %s", args.connect
        )
        server.poll_loop()
        LOGGER.info("connect-loop shut down completed")
    else:
        LOGGER.info(
            "Starting up %d workers connecting to %s", args.workers, args.connect
        )
        workers = [Thread(target=server.worker) for _ in range(args.workers)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
