"""Pydantic request/response models. Owner: Person A."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    session_id: str
    message: str
    lang: str = "en"          # en | tanglish | singlish

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    needs_input: bool = False
    service: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None

class ApproveRequest(BaseModel):
    # Approver identity is taken from the JWT; this optional note is for record only.
    note: Optional[str] = None


# --- Auth / RBAC ---------------------------------------------------------------
class RegisterRequest(BaseModel):
    nic: str
    full_name: str
    password: str

class LoginRequest(BaseModel):
    nic: str
    password: str

class UserOut(BaseModel):
    id: int
    kind: str
    nic: str
    full_name: str
    role: str
    services: List[str] = []
    jurisdiction: Optional[str] = None
    is_active: bool = True
    can_manage_users: bool = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class OfficerCreate(BaseModel):
    nic: str
    full_name: str
    password: str
    role: str                       # see app.auth.rbac.Role
    services: Optional[List[str]] = None   # defaults to role's services if omitted
    jurisdiction: Optional[str] = None     # e.g. "Divisional Secretariat"

class OfficerUpdate(BaseModel):
    full_name: Optional[str] = None
    services: Optional[List[str]] = None
    jurisdiction: Optional[str] = None
    is_active: Optional[bool] = None
