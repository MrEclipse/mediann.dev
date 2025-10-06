from pydantic import BaseModel
from datetime import datetime

"""Pydantic схемы для приложений"""


class ApplicationCreate(BaseModel):
    """Данные для создания приложения"""
    user_name: str
    description: str


class ApplicationRead(BaseModel):
    """Данные для чтения приложения"""
    id: int
    user_name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
