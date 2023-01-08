import secrets
import google.auth
from starlette.requests import Request
from opentelemetry import trace
from opentelemetry.trace import NonRecordingSpan
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider, SpanContext, RandomIdGenerator
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ALWAYS_ON


class Tracer(object):

    def __init__(self, request: Request):

        self._ctx = self._get_context(request)
        self._tracer = self._set_tracer()

    @property
    def project_id(self):

        credentials, project_id = google.auth.default()

        return project_id

    @property
    def trace_id(self):
        return self._ctx.get("trace_id")

    @property
    def span_id(self):
        return self._ctx.get("span_id")

    @property
    def flags(self):
        return self._ctx.get("flags")

    @property
    def trace(self):

        return f"projects/{self.project_id}/traces/{self.trace_id}"

    def start_span(self, name):

        span_context = SpanContext(
            trace_id=int(self.trace_id, base=16),
            span_id=RandomIdGenerator().generate_span_id(),
            is_remote=False,
        )

        ctx = trace.set_span_in_context(NonRecordingSpan(span_context))

        return self._tracer.start_as_current_span(name=name, context=ctx)

    @staticmethod
    def _set_tracer():

        tracer_provider = TracerProvider(sampler=ALWAYS_ON)  # always trace
        cloud_trace_exporter = CloudTraceSpanExporter()
        tracer_provider.add_span_processor(
            # BatchSpanProcessor buffers spans and sends them in batches in a
            # background thread. The default parameters are sensible, but can be
            # tweaked to optimize your performance
            BatchSpanProcessor(cloud_trace_exporter)
        )
        trace._set_tracer_provider(tracer_provider, False)

        return trace.get_tracer(__name__)

    @staticmethod
    def _get_context(request):

        ctx = {
            "trace_id": secrets.token_hex(16),
            "span_id": RandomIdGenerator().generate_span_id(),
            "flags": "o=1",
        }

        trace_context = request.headers.get('X-Cloud-Trace-Context', None)

        if trace_context is not None:

            ctx['trace_id'] = trace_context.split('/')[0]
            span = trace_context.split('/')[1].split(";")

            if len(span) > 1:
                ctx['span_id'] = span[0]
                ctx['flags'] = span[1]
            else:
                ctx['span_id'] = span[0]

        return ctx
