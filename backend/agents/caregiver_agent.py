from datetime import datetime, timedelta, timezone

from db.supabase_client import get_supabase
from services.alert_service import audit
from services.whatsapp_service import send_whatsapp_message


def notify_if_checkin_missed(patient: dict) -> list[dict]:
    last_check_in = patient.get("last_check_in_at")

    if last_check_in:
        try:
            parsed = datetime.fromisoformat(
                last_check_in.replace("Z", "+00:00")
            )

            if (
                datetime.now(timezone.utc) - parsed
                <= timedelta(hours=24)
            ):
                return []

        except ValueError:
            return []

    caregivers = (
        get_supabase()
        .table("caregivers")
        .select("*")
        .eq("patient_id", patient["id"])
        .eq("active", True)
        .execute()
        .data
    )

    results = []

    for caregiver in caregivers:
        if caregiver.get("preferred_language") == "es":
            message = (
                f"Hola {caregiver['full_name']}. "
                f"{patient['full_name']} no ha realizado un control "
                "en más de 24 horas. Por favor, comunícate con la persona "
                "y sigue el plan de atención."
            )
        else:
            message = (
                f"Hi {caregiver['full_name']}. "
                f"{patient['full_name']} has missed a check-in for more "
                "than 24 hours. Please contact them and follow the care plan."
            )

        provider_response = send_whatsapp_message(
            caregiver["phone"],
            message,
        )

        results.append(
            {
                "caregiver_id": caregiver["id"],
                "provider_response": provider_response,
            }
        )

    if results:
        audit(
            patient_id=patient["id"],
            actor="caregiver_agent",
            action="notified",
            entity_type="caregiver",
            entity_id=None,
            details={"count": len(results)},
        )

    return results
