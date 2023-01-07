""" Sensical overrides to Flask-Smorest, primarily around authentication
    and bootstrapping
"""
try:
    from flask_smorest import Blueprint as SmorestBlueprint, Api as SmorestApi
except Exception:
    Api = None
    Blueprint = None
else:
    from flask import abort, jsonify, render_template
    from webargs.flaskparser import FlaskParser

    class Api(SmorestApi):

        def __init__(self, *args, **kwargs):
            auth_decorator = kwargs.pop('auth_decorator', None)
            super(Api, self).__init__(*args, **kwargs)
            self._set_overrides(auth_decorator)

        def init_app(self, *args, **kwargs):
            auth_decorator = kwargs.pop('auth_decorator', None)
            super(Api, self).init_app(*args, **kwargs)
            self._set_overrides(auth_decorator)

        def _set_overrides(self, auth_decorator):
            if auth_decorator:
                self._openapi_swagger_ui =\
                    auth_decorator(self.__openapi_swagger_ui)
                self._openapi_redoc =\
                    auth_decorator(self._openapi_redoc)
                self._openapi_json =\
                    auth_decorator(self._openapi_json)
            else:
                self._openapi_swagger_ui = self.__openapi_swagger_ui

        # We override this funciton because we want to control how we customize
        # the swagger-ui template and title.
        def __openapi_swagger_ui(self):
            """Expose OpenAPI spec with Swagger UI"""
            return render_template(
                self._app.config.get('OPENAPI_SWAGGER_BASE_TEMPLATE',
                                     'swagger_ui.html'),
                title=self._app.config.get('OPENAPI_SWAGGER_APP_NAME',
                                           self._app.name),
                swagger_ui_url=self._swagger_ui_url,
            )

    class CustomParser(FlaskParser):
        DEFAULT_VALIDATION_STATUS = 400

        def handle_error(self, error, req, schema, error_status_code,
                         error_headers):
            """ Handles errors during parsing. Aborts the current HTTP request
                and responds with a 422 error.
            """

            # This is custom. If we have error messages, simply send them back
            if error.messages:
                msg = jsonify(error.messages)
                msg.status_code = self.DEFAULT_VALIDATION_STATUS
                return abort(msg)

            # Otherwise execute the base function
            return super(CustomParser,
                         self).handle_error(error, req, schema,
                                            error_status_code, error_headers)

    class Blueprint(SmorestBlueprint):
        ARGUMENTS_PARSER = CustomParser()
