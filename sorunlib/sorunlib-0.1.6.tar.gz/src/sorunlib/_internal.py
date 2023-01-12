"""Internal module for shared utilities within sorunlib.

The usual caveats apply, these interfaces might change without notice.

"""

import ocs


def check_response(response):
    """Check that a response from OCS indicates successful task/process
    completion.

    Args:
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.

    Raises:
        RuntimeError: When Operation has not completed successfully (either on
            initial request or after completion) or the response has timed out.

    """
    op = response.session['op_name']

    if response.status == ocs.ERROR:
        error = f"Request for Operation {op} failed.\n" + str(response)
        raise RuntimeError(error)
    elif response.status == ocs.TIMEOUT:
        error = f"Timeout reached waiting for {op} to complete." + str(
            response)
        raise RuntimeError(error)

    if not response.session['success']:
        error = 'Task failed to complete successfully.\n' + str(response)
        raise RuntimeError(error)
