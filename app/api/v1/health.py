from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_home() -> dict:
    """
    Health check endpoint for the root of the health API.
    """
    return {"status": "ok"}


@router.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Add more health-related endpoints as needed like conection to Rabbitmq, Redis, etc.
