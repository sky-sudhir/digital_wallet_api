from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str | None

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    username: str
    phone_number: str | None

    class Config:
        from_attributes = True