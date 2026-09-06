from functools import lru_cache
import httpx

from db.supabase_client import get_settings


@lru_cache
def get_http_client() -> httpx.Client:
    return httpx.Client(timeout=httpx.Timeout(20.0))


def normalize_phone_to_chat_id(phone: str) -> str:
    digits = "".join(character for character in phone if character.isdigit())
    if not digits:
        raise ValueError("Phone number does not contain any digits")
    return f"{digits}@c.us"


def send_whatsapp_message(phone: str, message: str) -> dict:
    settings = get_settings()

    if not settings.OPENWA_API_KEY:
        raise RuntimeError("OPENWA_API_KEY is not configured")

    chat_id = normalize_phone_to_chat_id(phone)
    url = (
        f"{settings.OPENWA_BASE_URL.rstrip('/')}"
        f"/sessions/{settings.OPENWA_SESSION_ID}"
        f"/messages/send-text"
    )

    response = get_http_client().post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": settings.OPENWA_API_KEY,
        },
        json={
            "chatId": chat_id,
            "text": message,
        },
    )
    response.raise_for_status()
    return response.json()
