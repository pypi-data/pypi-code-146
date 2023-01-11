from cubicweb.devtools.testlib import real_error_handling
from cubicweb.pyramid.test import PyramidCWTest


class WebCWTC(PyramidCWTest):
    def url_publish(self, url, data=None):
        """takes `url`, uses application's app_resolver to find the appropriate
        controller and result set, then publishes the result.

        To simulate post of www-form-encoded data, give a `data` dictionary
        containing desired key/value associations.

        This should pretty much correspond to what occurs in a real CW server
        except the apache-rewriter component is not called.
        """
        with self.admin_request_from_url(url) as req:
            if data is not None:
                req.form.update(data)
            ctrlid, rset = self.app.url_resolver.process(req, req.relative_path(False))
            return self.ctrl_publish(req, ctrlid, rset)

    def http_publish(self, url, data=None):
        """like `url_publish`, except this returns a http response, even in case
        of errors. You may give form parameters using the `data` argument.
        """
        with self.admin_request_from_url(url) as req:
            if data is not None:
                req.form.update(data)
            with real_error_handling(self.app):
                result = self.app_handle_request(req)
            return result, req

    def expect_redirect_handle_request(self, req, path="edit"):
        """call the publish method of the application publisher, expecting to
        get a Redirect exception
        """
        if req.relative_path(False) != path:
            req._url = path
        self.app_handle_request(req)
        self.assertTrue(300 <= req.status_out < 400, req.status_out)
        location = req.get_response_header("location")
        return self._parse_location(req, location)
