"""Authentication & officer-management routes. Owner: Person A.

Citizens self-register with NIC + password. Officers are created only by a Super-Admin.
Login returns a JWT plus the caller's scope so clients can tailor their UI.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.user import User
from app.models.schemas import (
    RegisterRequest, LoginRequest, LoginResponse, UserOut, OfficerCreate, OfficerUpdate,
)
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth import rbac
from app.auth.deps import get_current_user, require_super_admin

router = APIRouter(prefix="/auth", tags=["auth"])


def _to_out(user: User) -> UserOut:
    s = rbac.scope_summary(user)
    return UserOut(
        id=user.id, kind=user.kind, nic=user.nic, full_name=user.full_name,
        role=user.role, services=s["services"], jurisdiction=s["jurisdiction"],
        is_active=user.is_active, can_manage_users=s["can_manage_users"],
    )


def _by_nic(db: Session, nic: str) -> User | None:
    return db.exec(select(User).where(User.nic == nic)).first()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_session)):
    """Citizen self-registration. Officers cannot be created here."""
    if not req.nic.strip() or len(req.password) < 6:
        raise HTTPException(400, "NIC required and password must be >= 6 characters")
    if _by_nic(db, req.nic):
        raise HTTPException(409, "An account with this NIC already exists")
    user = User(
        kind="citizen", nic=req.nic.strip(), full_name=req.full_name.strip(),
        hashed_password=hash_password(req.password), role=rbac.Role.CITIZEN.value,
    )
    db.add(user); db.commit(); db.refresh(user)
    return LoginResponse(access_token=create_access_token(user.id), user=_to_out(user))


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_session)):
    user = _by_nic(db, req.nic.strip())
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(401, "Invalid NIC or password")
    if not user.is_active:
        raise HTTPException(403, "Account is deactivated")
    return LoginResponse(access_token=create_access_token(user.id), user=_to_out(user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return _to_out(user)


# --- Super-Admin: officer management ----------------------------------------------
@router.post("/officers", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_officer(req: OfficerCreate, _: User = Depends(require_super_admin),
                   db: Session = Depends(get_session)):
    try:
        role = rbac.Role(req.role)
    except ValueError:
        raise HTTPException(400, f"Unknown role '{req.role}'")
    if role not in rbac.OFFICER_ROLES:
        raise HTTPException(400, "Role is not an officer role")
    if _by_nic(db, req.nic):
        raise HTTPException(409, "An account with this NIC already exists")
    services = req.services if req.services is not None else rbac.default_services_for(req.role)
    user = User(
        kind="officer", nic=req.nic.strip(), full_name=req.full_name.strip(),
        hashed_password=hash_password(req.password), role=role.value,
        services=",".join(services), jurisdiction=req.jurisdiction,
    )
    db.add(user); db.commit(); db.refresh(user)
    return _to_out(user)


@router.get("/officers", response_model=list[UserOut])
def list_officers(_: User = Depends(require_super_admin), db: Session = Depends(get_session)):
    officers = db.exec(select(User).where(User.kind == "officer")).all()
    return [_to_out(o) for o in officers]


@router.patch("/officers/{officer_id}", response_model=UserOut)
def update_officer(officer_id: int, req: OfficerUpdate,
                   _: User = Depends(require_super_admin), db: Session = Depends(get_session)):
    officer = db.get(User, officer_id)
    if not officer or officer.kind != "officer":
        raise HTTPException(404, "Officer not found")
    if req.full_name is not None:
        officer.full_name = req.full_name
    if req.services is not None:
        officer.set_services(req.services)
    if req.jurisdiction is not None:
        officer.jurisdiction = req.jurisdiction or None
    if req.is_active is not None:
        officer.is_active = req.is_active
    db.add(officer); db.commit(); db.refresh(officer)
    return _to_out(officer)
