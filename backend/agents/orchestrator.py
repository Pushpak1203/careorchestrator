from datetime import datetime, timezone
from db.supabase_client import get_supabase
from agents.monitoring_agent import assess_patient
from agents.communication_agent import send_patient_outreach
from agents.escalation_agent import escalate
from agents.caregiver_agent import notify_if_checkin_missed
from services.alert_service import audit

def run_patient(patient_id: str) -> dict:
    db = get_supabase()
    patient = db.table("patients").select("*").eq("id", patient_id).single().execute().data
    assessment = assess_patient(patient_id).model_dump()
    db.table("patients").update({"risk_level": assessment["risk_level"], "updated_at": datetime.now(timezone.utc).isoformat()}).eq("id", patient_id).execute()

    outreach = None
    escalation = None
    if assessment["risk_level"] in {"MEDIUM", "HIGH", "CRITICAL"}:
        outreach = send_patient_outreach(patient, assessment)
    if assessment["risk_level"] in {"HIGH", "CRITICAL"}:
        escalation = escalate(patient, assessment)
    caregiver_notifications = notify_if_checkin_missed(patient)

    audit(patient_id, "orchestrator", "completed", "patient", patient_id, {"risk_level": assessment["risk_level"]})
    return {
        "patient_id": patient_id,
        "assessment": assessment,
        "outreach": outreach,
        "escalation": escalation,
        "caregiver_notifications": caregiver_notifications,
    }

def run_all_patients() -> list[dict]:
    patients = get_supabase().table("patients").select("id").execute().data
    results = []
    for patient in patients:
        try:
            results.append(run_patient(patient["id"]))
        except Exception as exc:
            results.append({"patient_id": patient["id"], "error": str(exc)})
    return results
