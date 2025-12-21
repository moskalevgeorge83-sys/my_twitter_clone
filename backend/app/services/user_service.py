"""Бизнес-логика работы с пользователями и подписками."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session


class UserService:
    @staticmethod
    def toggle_follow(
        db: Session, follower_id: int, target_id: int, action: str
    ) -> bool:
        """Переключает подписку/отписку (POST=подписка, DELETE=отписка)."""
        if follower_id == target_id:
            return False

        if action == "POST":
            # Проверяем дубликат
            existing = db.execute(
                text(
                    """
                SELECT 1 FROM follows 
                WHERE follower_id = :f AND following_id = :t
            """
                ),
                {"f": follower_id, "t": target_id},
            ).fetchone()

            if not existing:
                db.execute(
                    text(
                        """
                    INSERT INTO follows (follower_id, following_id) 
                    VALUES (:f, :t)
                """
                    ),
                    {"f": follower_id, "t": target_id},
                )
        else:  # DELETE
            db.execute(
                text(
                    """
                DELETE FROM follows 
                WHERE follower_id = :f AND following_id = :t
            """
                ),
                {"f": follower_id, "t": target_id},
            )

        db.commit()
        return True

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> dict:
        """Возвращает профиль пользователя с подписчиками/подписками."""
        user = db.execute(
            text("SELECT id, name FROM users WHERE id = :id"), {"id": user_id}
        ).first()
        if not user:
            raise HTTPException(404, "User not found")

        followers = db.execute(
            text(
                """
            SELECT u.id, u.name FROM users u
            JOIN follows f ON f.following_id = u.id
            WHERE f.follower_id = :user_id
        """
            ),
            {"user_id": user_id},
        ).fetchall()

        following = db.execute(
            text(
                """
            SELECT u.id, u.name FROM users u
            JOIN follows f ON f.follower_id = u.id
            WHERE f.following_id = :user_id
        """
            ),
            {"user_id": user_id},
        ).fetchall()

        return {
            "id": user.id,
            "name": user.name,
            "followers": [{"id": f[0], "name": f[1]} for f in followers],
            "following": [{"id": f[0], "name": f[1]} for f in following],
        }
