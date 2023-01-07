""" Response methods
"""
from flask import abort as flask_abort, make_response, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES


def abort(code, message=None, api_response=False):
    """ Properly abort the current request.

    Attaches `message` to response if given.

    :code int HTTP status code for abort
    :message str message Custom message to send with response
    :api_response boolean for responding to a webapp or an api
    :raise HTTPException:
    """
    try:
        if api_response:
            response = make_response(
                jsonify({
                    "code": code,
                    "message": message,
                    "status": HTTP_STATUS_CODES[code]
                }), code)
            flask_abort(response)
        else:
            flask_abort(code)
    except HTTPException as e:
        if message:
            e.data = {'message': str(message)}
        raise
