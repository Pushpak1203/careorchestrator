from fastapi import APIRouter, Depends, HTTPException
from api.deps import require_user
from db.supabase_client import get_supabase
from models.schemas import PatientCreate, PatientUpdate
from agents.orchestrator import run_patient

router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("")
def list_patients(_: dict = Depends(require_user)):
    return get_supabase().table("patients").select("*").order("created_at", desc=True).execute().data

@router.post("", status_code=201)
def create_patient(payload: PatientCreate, _: dict = Depends(require_user)):
    return get_supabase().table("patients").insert(payload.model_dump(mode="json")).execute().data[0]

@router.get("/{patient_id}")
def get_patient(patient_id: str, _: dict = Depends(require_user)):
    data = get_supabase().table("patients").select("*").eq("id", patient_id).execute().data
    if not data: raise HTTPException(404, "Patient not found")
    return data[0]

@router.patch("/{patient_id}")
def update_patient(patient_id: str, payload: PatientUpdate, _: dict = Depends(require_user)):
    values = payload.model_dump(mode="json", exclude_unset=True)
    data = get_supabase().table("patients").update(values).eq("id", patient_id).execute().data
    if not data: raise HTTPException(404, "Patient not found")
    return data[0]

@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: str, _: dict = Depends(require_user)):
    get_supabase().table("patients").delete().eq("id", patient_id).execute()

@router.post("/{patient_id}/run-agents")
def run_agents(patient_id: str, _: dict = Depends(require_user)):
    return run_patient(patient_id)
