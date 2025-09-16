from typing import Optional

from sqlmodel import Session, select

from app.models.client_application import ClientApplication
from app.schemas.client_applications import ClientApplicationCreate


class ClientApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, client_data: ClientApplicationCreate) -> ClientApplication:
        client = ClientApplication(**client_data.model_dump())
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def get_by_client_id(self, client_id: str) -> Optional[ClientApplication]:
        statement = select(ClientApplication).where(
            ClientApplication.client_id == client_id
        )
        return self.session.exec(statement).first()

    def list_all(self) -> list[ClientApplication]:
        return list(self.session.exec(select(ClientApplication)))
