from typing import Any
from db.supabase_client import get_supabase

def create_alert(patient_id: str, severity: str, title: str, message: str, source_agent: str, metadata: dict[str, Any] | None = None):
    db = get_supabase()
    payload = {
        "patient_id": patient_id,
        "severity": severity,
        "title": title,
        "message": message,
        "source_agent": source_agent,
        "metadata": metadata or {},
    }
    return db.table("alerts").insert(payload).execute().data[0]

def audit(patient_id: str | None, actor: str, action: str, entity_type: str, entity_id: str | None, details: dict[str, Any] | None = None):
    payload = {
        "patient_id": patient_id,
        "actor": actor,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "details": details or {},
    }
    return get_supabase().table("audit_log").insert(payload).execute().data[0]
