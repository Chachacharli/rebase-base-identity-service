from pydantic import BaseModel

class UserInfoSchema(BaseModel):
    sub: str
    username: str
    email: str
    email_verified: bool
