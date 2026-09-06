import os
from functools import lru_cache
from dataclasses import dataclass

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_service_role_key: str
    supabase_anon_key: str

    openrouter_api_key: str
    openrouter_model: str
    openrouter_base_url: str

    openwa_base_url: str
    openwa_api_key: str
    openwa_session_id: str

    frontend_origin: str
    orchestrator_interval_hours: int
    orchestrator_enabled: bool


@lru_cache()
def get_settings() -> Settings:
    supabase_url = os.getenv("SUPABASE_URL", "").strip()

    supabase_service_role_key = os.getenv(
        "SUPABASE_SERVICE_ROLE_KEY",
        ""
    ).strip()

    supabase_anon_key = os.getenv(
        "SUPABASE_ANON_KEY",
        ""
    ).strip()

    openrouter_api_key = os.getenv(
        "OPENROUTER_API_KEY",
        ""
    ).strip()

    openrouter_model = os.getenv(
        "OPENROUTER_MODEL",
        "openrouter/free"
    ).strip()

    openrouter_base_url = os.getenv(
        "OPENROUTER_BASE_URL",
        "https://openrouter.ai/api/v1"
    ).strip()

    openwa_base_url = os.getenv(
        "OPENWA_BASE_URL",
        ""
    ).strip().rstrip("/")

    openwa_api_key = os.getenv(
        "OPENWA_API_KEY",
        ""
    ).strip()

    openwa_session_id = os.getenv(
        "OPENWA_SESSION_ID",
        "careorchestrator"
    ).strip()

    frontend_origin = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:3000"
    ).strip()

    interval_value = os.getenv(
        "ORCHESTRATOR_INTERVAL_HOURS",
        "6"
    ).strip()

    enabled_value = os.getenv(
        "ORCHESTRATOR_ENABLED",
        "true"
    ).strip().lower()

    if not supabase_url:
        raise RuntimeError(
            "SUPABASE_URL is missing in backend/.env"
        )

    if not supabase_service_role_key:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY is missing in backend/.env"
        )

    if not supabase_url.startswith(
        ("https://", "http://")
    ):
        raise RuntimeError(
            "SUPABASE_URL must be a valid HTTP or HTTPS URL. "
            "Example: https://your-project.supabase.co"
        )

    try:
        orchestrator_interval_hours = int(interval_value)
    except ValueError as exc:
        raise RuntimeError(
            "ORCHESTRATOR_INTERVAL_HOURS must be an integer"
        ) from exc

    if orchestrator_interval_hours <= 0:
        raise RuntimeError(
            "ORCHESTRATOR_INTERVAL_HOURS must be greater than zero"
        )

    return Settings(
        supabase_url=supabase_url,
        supabase_service_role_key=supabase_service_role_key,
        supabase_anon_key=supabase_anon_key,

        openrouter_api_key=openrouter_api_key,
        openrouter_model=openrouter_model,
        openrouter_base_url=openrouter_base_url,

        openwa_base_url=openwa_base_url,
        openwa_api_key=openwa_api_key,
        openwa_session_id=openwa_session_id,

        frontend_origin=frontend_origin,
        orchestrator_interval_hours=orchestrator_interval_hours,
        orchestrator_enabled=enabled_value
        in {"true", "1", "yes", "on"},
    )


@lru_cache()
def get_supabase() -> Client:
    settings = get_settings()

    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )