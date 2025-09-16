from typing import List, Optional

from pydantic import BaseModel


class ClientApplicationCreate(BaseModel):
    display_name: str = "Unnamed Application"
    client_secret: Optional[str] = None
    redirect_uris: Optional[List[str]] = []
    post_logout_redirect_uris: Optional[List[str]] = []
    scopes: List[str] = ["openid", "profile", "email"]
    grant_types: List[str] = ["authorization_code"]
    is_public: bool = True
    tenant_id: Optional[str] = None


class ClientApplicationRead(BaseModel):
    id: str
    display_name: str
    client_id: str
    redirect_uris: List[str]
    post_logout_redirect_uris: Optional[List[str]]
    scopes: List[str]
    grant_types: List[str]
    is_public: bool
    tenant_id: Optional[str]

    class Config:
        from_attributes = True


class ClientApplicationUpdate(BaseModel):
    display_name: Optional[str]
    client_secret: Optional[str] = None
    redirect_uris: Optional[List[str]] = None
    post_logout_redirect_uris: Optional[List[str]] = None
    scopes: Optional[List[str]] = None
    grant_types: Optional[List[str]] = None
    is_public: Optional[bool] = None
    tenant_id: Optional[str] = None
