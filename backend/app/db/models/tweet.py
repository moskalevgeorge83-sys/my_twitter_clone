"""Модель твитов с поддержкой медиа и лайков."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..base import Base
from .tweet_media import tweet_media_table


class Tweet(Base):
    """Основная таблица твитов."""

    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(280), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Связь
    author = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete")

    medias = relationship(
        "Media", secondary=tweet_media_table, backref="tweets", cascade="all"
    )
