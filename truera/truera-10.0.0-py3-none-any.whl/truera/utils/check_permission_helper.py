from __future__ import annotations

import logging
from typing import Mapping, TYPE_CHECKING

import grpc

from truera.authn.usercontext import RequestContext
from truera.authn.usercontext import UserContext
from truera.client.private.rbac import ProjectAuth
from truera.protobuf.rbac.rbac_pb2 import \
    Privilege  # pylint: disable=no-name-in-module

if TYPE_CHECKING:
    from truera.authn.usercontext import RequestContextHelper
    from truera.client.private.rbac import Rbac

MOCK_REQUEST_CONTEXT = RequestContext(
    user_context=UserContext(
        id="test-id",
        name="test-name",
        tenant_id="tmp-tenant-id",
        email="test-email"
    ),
    request_id="test-request"
)


def authenticate_and_audit_request_analyzable(
    logger: logging.Logger, request_ctx_helper: RequestContextHelper,
    rbac_client: Rbac, context: grpc.ServicerContext, caller_name: str, *,
    project_id: str, **kwargs
) -> RequestContext:
    return _authenticate_and_audit_request(
        logger,
        request_ctx_helper,
        rbac_client,
        Privilege.PV_ANALYZE_PROJECT,
        context,
        caller_name,
        project_id=project_id,
        **kwargs
    )


def authenticate_and_audit_request_updateable(
    logger: logging.Logger, request_ctx_helper: RequestContextHelper,
    rbac_client: Rbac, context: grpc.ServicerContext, caller_name: str, *,
    project_id: str, **kwargs
) -> RequestContext:
    return _authenticate_and_audit_request(
        logger,
        request_ctx_helper,
        rbac_client,
        Privilege.PV_MODIFY_PROJECT,
        context,
        caller_name,
        project_id=project_id,
        **kwargs
    )


def authenticate_and_audit_request_viewable(
    logger: logging.Logger, request_ctx_helper: RequestContextHelper,
    rbac_client: Rbac, context: grpc.ServicerContext, caller_name: str, *,
    project_id: str, **kwargs
) -> RequestContext:
    return _authenticate_and_audit_request(
        logger,
        request_ctx_helper,
        rbac_client,
        Privilege.PV_VIEW_PROJECT,
        context,
        caller_name,
        project_id=project_id,
        **kwargs
    )


def _authenticate_and_audit_request(
    logger: logging.Logger, request_ctx_helper: RequestContextHelper,
    rbac_client: Rbac, privilege: Privilege, context: grpc.ServicerContext,
    caller_name: str, *, project_id: str, **kwargs
) -> RequestContext:
    audit_event = create_or_get_audit_event(context)
    request_ctx = request_ctx_helper.create_request_context_grpc(context)
    logger.info(f"{caller_name}: RequestContext= {request_ctx}")
    audit_event["project_id"] = project_id

    (
        ProjectAuth().set_rbac(rbac_client).set_grpc_context(context).
        set_request_context(request_ctx).set_project_id(project_id).
        check_privilege(privilege)
    )
    for kwarg, value in kwargs.items():
        audit_event[kwarg] = value
    return request_ctx


def create_or_get_audit_event(context: grpc.ServicerContext) -> Mapping:
    return context.audit_event if hasattr(context, "audit_event") else {}
