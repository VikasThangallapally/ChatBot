# Supabase uses PostgreSQL directly via PostgREST API
# We define User as a dictionary/Pydantic model instead of SQLAlchemy ORM
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password_hash: str

    class Config:
        from_attributes = True
