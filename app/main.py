from fastapi import FastAPI

from app.core.settings import get_settings
from app.routers.health import router as health_router
from app.routers.serial_number import router as serial_number_router

get_settings()

app = FastAPI(title="Serial Number Detection Agent")

app.include_router(health_router)
app.include_router(serial_number_router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Get the root endpoint.

    Returns:
        dict[str, str]: A simple greeting message.
    """
    return {"message": "Api is running"}
