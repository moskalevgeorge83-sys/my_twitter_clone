"""Модель лайков (user → tweet)."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..base import Base


class Like(Base):
    """Таблица лайков твитов пользователями."""

    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)

    # Двунаправленные связи
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")
