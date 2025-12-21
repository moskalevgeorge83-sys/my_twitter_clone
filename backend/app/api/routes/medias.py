"""Роут API для загрузки медиафайлов."""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ...api.dependencies import get_user_from_header
from ...db.base import get_db
from ...db.models.user import User
from ...schemas.media import MediaResponse
from ...services.media_service import MediaService

router = APIRouter(prefix="/medias", tags=["Medias"])


@router.post("/", response_model=MediaResponse)
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> MediaResponse:
    """Загружает медиафайл и возвращает его ID для привязки к твиту."""
    media_id = await MediaService.upload_media(file, db, current_user.id)
    return MediaResponse(result=True, media_id=media_id)
