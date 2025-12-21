"""Модель загруженных медиафайлов."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class Media(Base):
    """Таблица медиафайлов (изображения, видео)."""

    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Связь с владельцем файла
    user = relationship("User")
