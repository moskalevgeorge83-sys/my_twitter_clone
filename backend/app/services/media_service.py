"""Сервис загрузки и сохранения медиафайлов."""

import os
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..db.models.media import Media


class MediaService:
    @staticmethod
    async def upload_media(file: UploadFile, db: Session, user_id: int) -> int:
        """Загружает файл, сохраняет на диск и в БД.

        Args:
            file: Загружаемый файл
            db: SQLAlchemy сессия
            user_id: ID владельца файла

        Returns:
            ID созданной записи Media в БД
        """
        # Создаём директорию media
        os.makedirs("media", exist_ok=True)

        # Генерируем уникальное имя файла
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join("media", filename)

        # Сохраняем на диск
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)

        # Сохраняем метаданные в БД
        media = Media(
            file_path=filepath,
            file_name=file.filename,
            file_size=len(content),
            user_id=user_id,
        )
        db.add(media)
        db.flush()
        db.commit()

        return media.id
