"""Основная модель пользователя."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    """Таблица пользователей с API ключами для аутентификации."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    api_key = Column(String(50), unique=True, index=True, nullable=False)

    # Связи с другими моделями
    tweets = relationship("Tweet", back_populates="author")
    followers = relationship(
        "Follow", foreign_keys="Follow.follower_id", back_populates="follower"
    )
    following = relationship(
        "Follow", foreign_keys="Follow.following_id", back_populates="following"
    )
    likes = relationship("Like", back_populates="user")
