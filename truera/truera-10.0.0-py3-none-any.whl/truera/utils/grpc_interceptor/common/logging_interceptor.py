import logging
import sched
from threading import Thread
import time

from truera.utils.grpc_interceptor import base as grpc_interceptor_base
from truera.utils.timing_logger import TimingLogger


def _print_rpc(start_time, rpc_name, state, request):
    if state['state'] != 'RUNNING':
        return
    duration = time.time() - start_time
    logging.getLogger(__name__).warn(
        "RPC %s running for %f seconds(Started at %d).\n Request: %s", rpc_name,
        duration, start_time, request
    )


class InfiniteSchedulerThread(Thread):

    def __init__(self, scheduler):
        super(InfiniteSchedulerThread, self).__init__()
        super(InfiniteSchedulerThread, self).setDaemon(True)
        self.scheduler = scheduler

    def run(self):
        while True:
            self.scheduler.run()
            time.sleep(0.2)


class LoggingServerInterceptor(
    grpc_interceptor_base.UnaryServerInterceptor,
    grpc_interceptor_base.StreamServerInterceptor
):
    """An interceptor that logs gRPC calls.
    
       RPC names and times are logged for every RPC. For failed RPCs, the exception
       is also logged.
    """

    def __init__(self, log_rpcs_after=10):
        self.logger = logging.getLogger('ailens.LoggingServerInterceptor')
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler_thread = InfiniteSchedulerThread(self.scheduler)
        self.scheduler_thread.start()
        self.log_rpcs_after = log_rpcs_after

    def intercept_unary(self, request, servicer_context, server_info, handler):
        state = {'state': 'RUNNING'}
        friendly_name = servicer_context.friendly_name
        with TimingLogger('RPC:' + friendly_name) as _:
            if self.log_rpcs_after:
                self.scheduler.enter(
                    self.log_rpcs_after, 1, _print_rpc,
                    (time.time(), friendly_name, state, request)
                )

            try:
                response = handler(request, servicer_context)
            finally:
                # Useful for logging of RPCs that were explicitly aborted (instead of failed
                # due to unexpected exceptions.)
                state['state'] = 'DONE'
                if servicer_context.is_aborted:
                    self.logger.error(
                        "RPC %s aborted with code %s and message: %s",
                        friendly_name, servicer_context.code,
                        servicer_context.details
                    )
                    return
            return response

    def intercept_stream(
        self, request_or_iterator, servicer_context, server_info, handler
    ):
        # TODO(apoorv): Add logging for stream calls.
        response = handler(request_or_iterator, servicer_context)
        return response
