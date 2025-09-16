from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.client_application_repository import ClientApplicationRepository
from app.schemas.client_applications import (
    ClientApplicationCreate,
    ClientApplicationRead,
    ClientApplicationUpdate,
)
from app.services.client_application_service import ClientService

router = APIRouter()


@router.get("/client_applications", response_model=List[ClientApplicationRead])
def list_clients(session: Session = Depends(get_session)):
    repository = ClientApplicationRepository(session)
    service = ClientService(repository)
    return service.list_clients()


@router.get("/client_applications/{client_id}", response_model=ClientApplicationRead)
def get_client(client_id: str, session: Session = Depends(get_session)):
    repository = ClientApplicationRepository(session)
    service = ClientService(repository)
    client = service.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post(
    "/client_applications",
    response_model=ClientApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def register_client(
    client_data: ClientApplicationCreate,
    session: Session = Depends(get_session),
):
    repository = ClientApplicationRepository(session)
    service = ClientService(repository)
    try:
        client = service.register_client(client_data)
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/client_applications/{client_id}", response_model=ClientApplicationRead)
def update_client(
    client_id: str,
    client_data: ClientApplicationUpdate,
    session: Session = Depends(get_session),
):
    repository = ClientApplicationRepository(session)
    service = ClientService(repository)
    client = service.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in client_data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)

    session.add(client)
    session.commit()
    session.refresh(client)
    return client
