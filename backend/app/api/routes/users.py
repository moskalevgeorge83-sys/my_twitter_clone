"""Роуты API для работы с пользователями и подписками."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ...api.dependencies import get_user_from_header
from ...db.base import get_db
from ...db.models.user import User
from ...services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=dict)
async def get_me(
    current_user: User = Depends(get_user_from_header), db: Session = Depends(get_db)
) -> dict:
    """Возвращает профиль текущего авторизованного пользователя."""
    profile = UserService.get_user_profile(db, current_user.id)
    return {"result": True, "user": profile}


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """Возвращает профиль пользователя + статус подписки для текущего."""
    profile = UserService.get_user_profile(db, user_id)

    if current_user.id != user_id:
        followers_count = db.execute(
            text("SELECT COUNT(*) FROM follows WHERE following_id = :user_id"),
            {"user_id": user_id},
        ).scalar()

        is_following = (
            db.execute(
                text(
                    """
                SELECT 1 FROM follows
                WHERE follower_id = :follower_id AND following_id = :user_id
            """
                ),
                {"follower_id": current_user.id, "user_id": user_id},
            ).fetchone()
            is not None
        )

        profile["followers_count"] = followers_count
        profile["is_following"] = is_following

    return {"result": True, "user": profile}


@router.post("/{user_id}/follow", response_model=dict)
async def toggle_follow(
    user_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """Переключает подписку/отписку (POST) в пределах единого endpoint."""
    if current_user.id == user_id:
        return {"result": True}

    existing = db.execute(
        text(
            """
        SELECT 1 FROM follows
        WHERE follower_id = :follower_id AND following_id = :user_id
    """
        ),
        {"follower_id": current_user.id, "user_id": user_id},
    ).fetchone()

    if existing:
        db.execute(
            text(
                """
            DELETE FROM follows
            WHERE follower_id = :follower_id AND following_id = :user_id
        """
            ),
            {"follower_id": current_user.id, "user_id": user_id},
        )
    else:
        db.execute(
            text(
                """
            INSERT INTO follows (follower_id, following_id)
            VALUES (:follower_id, :user_id)
        """
            ),
            {"follower_id": current_user.id, "user_id": user_id},
        )

    db.commit()
    return {"result": True}


@router.delete("/{user_id}/follow", response_model=dict)
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """Отписывается от пользователя (DELETE) в случае кнопки 'перестать читать!'"""
    if not current_user or current_user.id == user_id:
        return {"result": False, "error": "Cannot unfollow yourself"}

    result = db.execute(
        text(
            """
        DELETE FROM follows 
        WHERE follower_id = :follower_id AND following_id = :user_id
    """
        ),
        {"follower_id": current_user.id, "user_id": user_id},
    )

    db.commit()
    return {"result": result.rowcount > 0}
