from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Checks for system health.

    Returns:
        HealthResponse: Health status payload.
    """
    return HealthResponse(status="ok")
