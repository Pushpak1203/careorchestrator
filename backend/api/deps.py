from typing import Dict, Optional

from fastapi import Header, HTTPException


async def require_user(
    authorization: Optional[str] = Header(default=None),
) -> Dict[str, str]:
    """
    Temporary authentication dependency for local MVP development.

    The application currently allows unauthenticated local requests so that
    the MVP can be tested without implementing the complete Supabase login
    flow.

    If an Authorization header is provided, its format is validated.

    This must be replaced with strict Supabase JWT validation before
    production deployment.
    """

    if not authorization:
        return {
            "id": "local-mvp-user",
            "email": "local@careorchestrator.mvp",
            "role": "mvp",
        }

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header. Expected Bearer token.",
        )

    token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is empty.",
        )

    return {
        "id": "authenticated-mvp-user",
        "role": "authenticated",
    }


async def get_current_user(
    authorization: Optional[str] = Header(default=None),
) -> Dict[str, str]:
    """
    Compatibility alias for route modules that use get_current_user.
    """

    return await require_user(authorization)