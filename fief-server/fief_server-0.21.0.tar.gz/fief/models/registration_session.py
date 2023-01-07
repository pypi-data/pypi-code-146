import secrets
from enum import Enum

from pydantic import UUID4
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String

from fief.models.base import WorkspaceBase
from fief.models.generics import GUID, CreatedUpdatedAt, ExpiresAt, UUIDModel
from fief.models.oauth_account import OAuthAccount
from fief.models.tenant import Tenant
from fief.settings import settings


class RegistrationSessionFlow(str, Enum):
    PASSWORD = "PASSWORD"
    OAUTH = "OAUTH"


class RegistrationSession(UUIDModel, CreatedUpdatedAt, ExpiresAt, WorkspaceBase):
    __tablename__ = "registration_sessions"
    __lifetime_seconds__ = settings.registration_session_lifetime_seconds

    token: str = Column(
        String(length=255),
        default=secrets.token_urlsafe,
        nullable=False,
        index=True,
        unique=True,
    )

    flow: RegistrationSessionFlow = Column(
        String(length=255), default=RegistrationSessionFlow.PASSWORD, nullable=False
    )

    email: str | None = Column(String(length=320), nullable=True)

    oauth_account_id: UUID4 | None = Column(
        GUID, ForeignKey(OAuthAccount.id, ondelete="CASCADE"), nullable=True
    )
    oauth_account: OAuthAccount | None = relationship("OAuthAccount", lazy="joined")

    tenant_id: UUID4 = Column(
        GUID, ForeignKey(Tenant.id, ondelete="CASCADE"), nullable=False
    )
    tenant: Tenant = relationship("Tenant")
