from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from api.deps import require_user
from db.supabase_client import get_supabase
from models.schemas import AlertUpdate

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
def list_alerts(status: str | None = None, _: dict = Depends(require_user)):
    q = get_supabase().table("alerts").select("*, patients(full_name)").order("created_at", desc=True)
    if status: q = q.eq("status", status)
    return q.execute().data

@router.get("/{alert_id}")
def get_alert(alert_id: str, _: dict = Depends(require_user)):
    rows = get_supabase().table("alerts").select("*").eq("id", alert_id).execute().data
    if not rows: raise HTTPException(404, "Alert not found")
    return rows[0]

@router.patch("/{alert_id}")
def update_alert(alert_id: str, payload: AlertUpdate, _: dict = Depends(require_user)):
    values = {"status": payload.status}
    now = datetime.now(timezone.utc).isoformat()
    if payload.status == "ACKNOWLEDGED": values["acknowledged_at"] = now
    if payload.status == "RESOLVED": values["resolved_at"] = now
    rows = get_supabase().table("alerts").update(values).eq("id", alert_id).execute().data
    if not rows: raise HTTPException(404, "Alert not found")
    return rows[0]
