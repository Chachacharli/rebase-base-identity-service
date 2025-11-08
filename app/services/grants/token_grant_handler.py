from abc import ABC, abstractmethod
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.domain.tokens.token_response import GrantTokenResponse


class TokenGrantHandler(ABC):
    def __init__(self, settings: Settings, session: Session):
        self.settings = settings
        self.session = session

    @abstractmethod
    def handle(self, form_data: Dict[str, Any]) -> GrantTokenResponse:
        pass
