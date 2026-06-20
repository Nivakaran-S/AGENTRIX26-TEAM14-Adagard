"""REST routes — thin layer over the agent graph. Owner: Person A.
Implements the endpoints defined in /API_CONTRACT.md, now behind RBAC."""
from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import ChatRequest, ChatResponse, ApproveRequest
from app.models.user import User
from app.graph.graph import run_turn
from app.models.store import VERIFICATIONS
from app.auth.deps import require_citizen, require_officer
from app.auth import rbac

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, citizen: User = Depends(require_citizen)):
    result = run_turn(req.session_id, req.message, req.lang)
    return result


@router.get("/verifications")
def list_verifications(officer: User = Depends(require_officer)):
    """Pending packets the officer is scoped to see (Super-Admin sees all)."""
    return [
        v for v in VERIFICATIONS.values()
        if not v["approved"]
        and rbac.can_act(officer, v.get("service"), (v.get("plan") or {}).get("office"))
    ]


@router.post("/verifications/{vid}/approve")
def approve(vid: str, officer: User = Depends(require_officer), body: ApproveRequest | None = None):
    packet = VERIFICATIONS.get(vid)
    if packet is None:
        raise HTTPException(status_code=404, detail="verification not found")
    if not rbac.can_act(officer, packet.get("service"), (packet.get("plan") or {}).get("office")):
        raise HTTPException(status_code=403, detail="packet is outside your service/jurisdiction")
    packet["approved"] = True
    packet["officer"] = officer.full_name          # server-trusted identity from the JWT
    packet["officer_nic"] = officer.nic
    return {"ok": True}
