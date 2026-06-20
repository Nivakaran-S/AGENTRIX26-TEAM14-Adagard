"""FastAPI auth dependencies. Owner: Person A.

`get_current_user` decodes the Bearer JWT and loads the user from the DB on every request
(so deactivation / role changes take effect immediately). The require_* dependencies layer
route-level RBAC on top.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.db import get_session
from app.models.user import User
from app.auth.security import decode_token
from app.auth import rbac

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

_UNAUTH = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)
_FORBIDDEN = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted")


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> User:
    if not token:
        raise _UNAUTH
    claims = decode_token(token)
    if not claims or "sub" not in claims:
        raise _UNAUTH
    user = db.get(User, int(claims["sub"]))
    if not user or not user.is_active:
        raise _UNAUTH
    return user


def require_citizen(user: User = Depends(get_current_user)) -> User:
    if user.kind != "citizen":
        raise _FORBIDDEN
    return user


def require_officer(user: User = Depends(get_current_user)) -> User:
    if user.role not in {r.value for r in rbac.OFFICER_ROLES}:
        raise _FORBIDDEN
    return user


def require_super_admin(user: User = Depends(get_current_user)) -> User:
    if not rbac.is_super_admin(user):
        raise _FORBIDDEN
    return user
