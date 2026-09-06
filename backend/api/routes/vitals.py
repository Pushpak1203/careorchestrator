from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from api.deps import require_user
from db.supabase_client import get_supabase
from models.schemas import VitalCreate

router = APIRouter(prefix="/vitals", tags=["vitals"])

@router.post("", status_code=201)
def ingest_vitals(payload: VitalCreate, _: dict = Depends(require_user)):
    patient = get_supabase().table("patients").select("id").eq("id", str(payload.patient_id)).execute().data
    if not patient: raise HTTPException(404, "Patient not found")
    data = payload.model_dump(mode="json")
    if data.get("recorded_at") is None: data["recorded_at"] = datetime.now(timezone.utc).isoformat()
    created = get_supabase().table("vitals").insert(data).execute().data[0]
    get_supabase().table("patients").update({"last_check_in_at": datetime.now(timezone.utc).isoformat()}).eq("id", str(payload.patient_id)).execute()
    return created

@router.get("/patient/{patient_id}")
def patient_vitals(patient_id: str, limit: int = 100, _: dict = Depends(require_user)):
    return get_supabase().table("vitals").select("*").eq("patient_id", patient_id).order("recorded_at", desc=False).limit(min(max(limit, 1), 500)).execute().data

@router.delete("/{vital_id}", status_code=204)
def delete_vital(vital_id: str, _: dict = Depends(require_user)):
    get_supabase().table("vitals").delete().eq("id", vital_id).execute()
