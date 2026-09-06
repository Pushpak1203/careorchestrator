from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from db.supabase_client import get_settings
from services.whatsapp_service import send_whatsapp_message


def get_llm() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=0.2,
    )


def fallback_message(language: str, name: str, risk_level: str) -> str:
    english = {
        "LOW": (
            f"Hi {name}. Your recent check-in looks stable. "
            "Please continue following your care plan."
        ),
        "MEDIUM": (
            f"Hi {name}. We noticed a change in your recent health readings. "
            "Please review your care plan and complete a check-in soon."
        ),
        "HIGH": (
            f"Hi {name}. Your recent readings need prompt attention. "
            "Please contact your clinical team as soon as possible."
        ),
        "CRITICAL": (
            f"Hi {name}. Your recent readings may require urgent clinical attention. "
            "If you feel unwell, seek emergency medical help immediately."
        ),
    }

    spanish = {
        "LOW": (
            f"Hola {name}. Tu control reciente parece estable. "
            "Continúa siguiendo tu plan de atención."
        ),
        "MEDIUM": (
            f"Hola {name}. Detectamos un cambio en tus mediciones recientes. "
            "Revisa tu plan de atención y realiza un control pronto."
        ),
        "HIGH": (
            f"Hola {name}. Tus mediciones recientes requieren atención pronta. "
            "Comunícate con tu equipo clínico lo antes posible."
        ),
        "CRITICAL": (
            f"Hola {name}. Tus mediciones recientes pueden requerir atención clínica urgente. "
            "Si te sientes mal, busca ayuda médica de emergencia inmediatamente."
        ),
    }

    messages = spanish if language == "es" else english
    return messages[risk_level]


def generate_personalized_message(
    patient: dict,
    assessment: dict,
) -> str:
    fallback = fallback_message(
        patient.get("preferred_language", "en"),
        patient["full_name"],
        assessment["risk_level"],
    )

    language = (
        "Spanish"
        if patient.get("preferred_language") == "es"
        else "English"
    )

    try:
        llm = get_llm()

        prompt = f"""
Write one concise WhatsApp message for a chronic-care patient.

Language: {language}
Patient name: {patient["full_name"]}
Risk level: {assessment["risk_level"]}
Monitoring reasons: {assessment["reasons"]}

Rules:
- Do not diagnose the patient.
- Do not invent clinical facts.
- Do not prescribe medication.
- Do not change the risk level.
- Keep the message empathetic and concise.
- Clearly communicate the appropriate urgency.
- Maximum 450 characters.
"""

        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You write safe, concise patient communication. "
                        "Clinical severity is supplied by deterministic software "
                        "and must never be changed."
                    )
                ),
                HumanMessage(content=prompt),
            ]
        )

        if isinstance(response.content, str) and response.content.strip():
            return response.content.strip()[:450]

    except Exception:
        return fallback

    return fallback


def send_patient_outreach(
    patient: dict,
    assessment: dict,
) -> dict:
    message = generate_personalized_message(patient, assessment)

    result = send_whatsapp_message(
        patient["phone"],
        message,
    )

    return {
        "channel": "whatsapp",
        "message": message,
        "provider_response": result,
    }
