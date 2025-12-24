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
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """
    Подписывает *user_id* на *current_user*.

    ВАЖНО: логика инвертирована относительно классического сценария:
    - user_id трактуется как "подписчик" (читатель),
    - current_user трактуется как "подписуемый" (того, кого читают).
    Такой контракт ожидает фронтенд, поэтому follower_id = user_id,
    а following_id = current_user.id.
    """
    if current_user.id == user_id:
        return {"result": False, "error": "Нельзя подписаться на самого себя"}

    existing = db.execute(
        text(
            """
            SELECT 1 FROM follows
            WHERE follower_id = :follower_id AND following_id = :following_id
        """
        ),
        {"follower_id": user_id, "following_id": current_user.id},
    ).fetchone()

    if existing:
        return {"result": True, "message": "Уже подписан"}

    db.execute(
        text(
            """
            INSERT INTO follows (follower_id, following_id)
            VALUES (:follower_id, :following_id)
        """
        ),
        {"follower_id": user_id, "following_id": current_user.id},
    )
    db.commit()
    return {"result": True, "action": "followed"}


@router.delete("/{user_id}/follow", response_model=dict)
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """
    Отписывает *user_id* от *current_user*.

    Сохраняется та же инвертированная модель:
    - user_id — это подписчик,
    - current_user — тот, от кого отписываются.
    Удаляется запись, где follower_id = user_id и following_id = current_user.id.
    """
    if current_user.id == user_id:
        return {"result": False, "error": "Нельзя отписаться от самого себя"}

    result = db.execute(
        text(
            """
            DELETE FROM follows
            WHERE follower_id = :follower_id AND following_id = :following_id
        """
        ),
        {"follower_id": user_id, "following_id": current_user.id},
    )
    db.commit()

    if result.rowcount > 0:
        return {"result": True, "action": "unfollowed"}
    return {"result": False, "error": "Подписка не найдена"}
