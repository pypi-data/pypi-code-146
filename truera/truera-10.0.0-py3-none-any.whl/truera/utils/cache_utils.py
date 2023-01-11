import uuid

from truera.authn.usercontext import RequestContext


def get_or_create_request_id(request_context: RequestContext) -> str:
    ret = request_context.get_request_id()
    if not ret:
        ret = f"{uuid.uuid4()}_INFERRED"
    return ret
