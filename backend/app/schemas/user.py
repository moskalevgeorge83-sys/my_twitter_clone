"""Pydantic схемы для профилей пользователей."""

from typing import List

from pydantic import BaseModel


class UserOut(BaseModel):
    """Схема профиля пользователя с подписками."""

    id: int
    name: str
    followers: List[dict]
    following: List[dict]

    class Config:
        from_attributes = True
