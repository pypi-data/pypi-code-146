from flask import Flask, request
from opentelemetry.semconv.trace import SpanAttributes

from opentelemetry import trace


class DigmaFlaskInstrumentor:

    @staticmethod
    def instrument_app(app: Flask):
        if not hasattr(app, "_is_instrumented_by_opentelemetry") or app._is_instrumented_by_opentelemetry == False:
           raise Exception("Digma requires your Flask server to be instrumented. To use the Digma Flask instrumentation please make sure to use the FlaskInstrumentor.instrument() method first.")
        before_request = DigmaFlaskInstrumentor._before_request_wrapped(app)
        app.before_request ( before_request)



    @staticmethod
    def _before_request_wrapped(app):

        def before_request():

            span = trace.get_current_span()
            if span and span.is_recording():

                adapter = app.url_map.bind(request.host)
                match = adapter.match(request.url_rule, method=request.method)
                mapped_view = app.view_functions[match[0]], match[1]
                if (mapped_view != None):
                    view_func = mapped_view[0]
                    span.set_attribute(SpanAttributes.CODE_NAMESPACE, view_func.__module__)
                    span.set_attribute(SpanAttributes.CODE_FUNCTION, view_func.__qualname__)
                    span.set_attribute(SpanAttributes.CODE_FILEPATH, view_func.__code__.co_filename)
                    span.set_attribute(SpanAttributes.CODE_LINENO, view_func.__code__.co_firstlineno)

        return before_request

