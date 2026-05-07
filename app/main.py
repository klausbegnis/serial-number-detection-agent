from fastapi import FastAPI

from app.routers.health import router as health_router

app = FastAPI(title="Serial Number Detection Agent")

app.include_router(health_router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Get the root endpoint.

    Returns:
        dict[str, str]: A simple greeting message.
    """
    return {"message": "Api is running"}
