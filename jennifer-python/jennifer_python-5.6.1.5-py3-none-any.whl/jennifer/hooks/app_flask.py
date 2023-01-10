from jennifer.api.format import format_function
from jennifer.agent import jennifer_agent
from jennifer.wrap.wsgi import wrap_wsgi_app
from distutils.version import LooseVersion

__hooking_module__ = 'flask'
__minimum_python_version__ = LooseVersion("2.7")


def wrap_dispatch_request(origin, flask):

    def handler(self):
        try:
            from werkzeug.exceptions import NotFound
        except ImportError:
            NotFound = None

        return_value = None
        err = None

        try:
            return_value = origin(self)
        except Exception as e:
            err = e

        if err is not None:
            try:
                current_tx = jennifer_agent().current_transaction()

                if current_tx is not None:
                    profiler = current_tx.profiler

                    if type(err) == NotFound:
                        profiler.not_found(err)
                    else:
                        profiler.service_error(err)
            except:
                pass

            raise err

        return return_value

    return handler


def hook(flask):
    flask.Flask.wsgi_app = wrap_wsgi_app(flask.Flask.wsgi_app)
    flask.Flask.dispatch_request = wrap_dispatch_request(flask.Flask.dispatch_request, flask)
