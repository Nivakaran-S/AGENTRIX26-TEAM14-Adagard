"""User/officer table. Owner: Person A.

One table for both principal kinds. Authorization is data-driven: `role` is a display
label while `services` (CSV of service keys) + `jurisdiction` are the enforced scope.
Citizens have kind='citizen', role='CITIZEN', empty scope.
"""
from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import SQLModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kind: str = Field(index=True)                 # "citizen" | "officer"
    nic: str = Field(index=True, unique=True)     # login identifier
    full_name: str
    hashed_password: str
    role: str = "CITIZEN"                          # see app.auth.rbac.Role
    services: str = ""                            # CSV of service keys (officers)
    jurisdiction: Optional[str] = None            # DS / Kachcheri office tier, or None=all
    is_active: bool = True
    created_at: datetime = Field(default_factory=_utcnow)

    # --- convenience accessors --------------------------------------------------
    @property
    def service_list(self) -> List[str]:
        return [s for s in (self.services or "").split(",") if s]

    def set_services(self, services: List[str]) -> None:
        self.services = ",".join(services)
