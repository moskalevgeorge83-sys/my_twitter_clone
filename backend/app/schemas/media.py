"""Pydantic схемы для API ответов медиа."""

from pydantic import BaseModel


class MediaResponse(BaseModel):
    """Ответ на запрос загрузки медиафайла."""

    result: bool
    media_id: int
