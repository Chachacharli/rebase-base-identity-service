from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AppSettingCreate(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class AppSettingRead(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class AppSettingUpdate(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
