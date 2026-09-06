from fastapi import APIRouter, Depends, HTTPException
from api.deps import require_user
from db.supabase_client import get_supabase
from models.schemas import CaregiverCreate, CaregiverUpdate

router = APIRouter(prefix="/caregivers", tags=["caregivers"])

@router.get("/patient/{patient_id}")
def list_caregivers(patient_id: str, _: dict = Depends(require_user)):
    return get_supabase().table("caregivers").select("*").eq("patient_id", patient_id).order("created_at").execute().data

@router.post("", status_code=201)
def assign_caregiver(payload: CaregiverCreate, _: dict = Depends(require_user)):
    return get_supabase().table("caregivers").insert(payload.model_dump(mode="json")).execute().data[0]

@router.patch("/{caregiver_id}")
def update_caregiver(caregiver_id: str, payload: CaregiverUpdate, _: dict = Depends(require_user)):
    values = payload.model_dump(exclude_unset=True)
    rows = get_supabase().table("caregivers").update(values).eq("id", caregiver_id).execute().data
    if not rows: raise HTTPException(404, "Caregiver not found")
    return rows[0]

@router.delete("/{caregiver_id}", status_code=204)
def remove_caregiver(caregiver_id: str, _: dict = Depends(require_user)):
    get_supabase().table("caregivers").delete().eq("id", caregiver_id).execute()
