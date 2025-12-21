"""Pydantic схемы для твитов (запрос/ответ)."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TweetCreate(BaseModel):
    """Входная схема для создания твита."""

    tweet_data: str
    tweet_media_ids: Optional[List[int]] = []


class TweetOut(BaseModel):
    """Выходная схема твита с вложениями и лайками."""

    id: int
    content: str
    created_at: datetime
    attachments: List[str]
    author: dict
    likes: List[dict]

    class Config:
        from_attributes = True
