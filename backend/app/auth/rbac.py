"""Role-based access control: roles, default scopes, and the object-level rule. Owner: Person A.

Authorization has three layers used across the app:
  1. route-level   — citizen vs officer vs super-admin (see app.auth.deps)
  2. object-level   — can_act(user, packet): service + jurisdiction scoping (here)
  3. capability     — can_manage_users(user): officer CRUD (here)

Scope is data-driven: each officer row stores its own `services` + `jurisdiction`, so the
Role below is just a label + the default scope used when seeding/creating officers.
"""
from enum import Enum
from typing import List, Optional

from app.graph import knowledge
from app.models.user import User


class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    REGISTRAR = "REGISTRAR"                 # birth/death civil registry (jurisdiction-scoped)
    DRP_OFFICER = "DRP_OFFICER"             # NIC
    IMMIGRATION_OFFICER = "IMMIGRATION_OFFICER"  # passport
    GRAMA_NILADHARI = "GRAMA_NILADHARI"     # GN certificate
    DMT_EXAMINER = "DMT_EXAMINER"           # driving licence
    CITIZEN = "CITIZEN"


OFFICER_ROLES = {
    Role.REGISTRAR, Role.DRP_OFFICER, Role.IMMIGRATION_OFFICER,
    Role.GRAMA_NILADHARI, Role.DMT_EXAMINER, Role.SUPER_ADMIN,
}

# Default service scope per role (keys come from knowledge.SERVICES).
ROLE_SERVICES = {
    Role.REGISTRAR: ["birth_cert", "death_cert"],
    Role.DRP_OFFICER: ["nic"],
    Role.IMMIGRATION_OFFICER: ["passport"],
    Role.GRAMA_NILADHARI: ["gn_cert"],
    Role.DMT_EXAMINER: ["license"],
    Role.SUPER_ADMIN: list(knowledge.SERVICES),   # all
    Role.CITIZEN: [],
}


def is_super_admin(user: User) -> bool:
    return user.role == Role.SUPER_ADMIN.value


def can_manage_users(user: User) -> bool:
    return is_super_admin(user)


def can_act(user: User, service: Optional[str], office: Optional[str]) -> bool:
    """Object-level rule for a verification packet (its service + plan.office tier)."""
    if is_super_admin(user):
        return True
    if user.kind != "officer":
        return False
    if service is not None and service not in user.service_list:
        return False
    # jurisdiction None => the officer covers all office tiers for their services.
    if user.jurisdiction and office and user.jurisdiction != office:
        return False
    return True


def scope_summary(user: User) -> dict:
    """Compact scope description returned to clients (drives admin-web UI)."""
    return {
        "role": user.role,
        "services": user.service_list if user.kind == "officer" else [],
        "jurisdiction": user.jurisdiction,
        "can_manage_users": can_manage_users(user),
    }


def default_services_for(role: str) -> List[str]:
    try:
        return list(ROLE_SERVICES[Role(role)])
    except (ValueError, KeyError):
        return []
