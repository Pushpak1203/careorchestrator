from services.alert_service import audit, create_alert
from services.whatsapp_service import send_whatsapp_message


def escalate(patient: dict, assessment: dict) -> dict | None:
    if assessment["risk_level"] not in {"HIGH", "CRITICAL"}:
        return None

    title = (
        f"{assessment['risk_level']} risk detected for "
        f"{patient['full_name']}"
    )

    message = "; ".join(assessment["reasons"])

    alert = create_alert(
        patient_id=patient["id"],
        severity=assessment["risk_level"],
        title=title,
        message=message,
        source_agent="escalation_agent",
        metadata={"assessment": assessment},
    )

    clinician_result = None
    clinician_phone = patient.get("clinician_phone")

    if clinician_phone:
        clinician_result = send_whatsapp_message(
            clinician_phone,
            f"{title}. {message}",
        )

    audit(
        patient_id=patient["id"],
        actor="escalation_agent",
        action="created",
        entity_type="alert",
        entity_id=alert["id"],
        details={
            "severity": assessment["risk_level"],
            "clinician_notified": clinician_result is not None,
        },
    )

    return {
        "alert": alert,
        "clinician_notification": clinician_result,
    }
