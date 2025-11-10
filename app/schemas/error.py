from typing import Dict, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict] = None
    code: Optional[str] = None
