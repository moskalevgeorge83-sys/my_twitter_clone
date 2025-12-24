"""Бизнес-логика работы с твитами (CRUD + лайки + лента)."""

from fastapi import HTTPException, status
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from ..core.errors import Forbidden, TweetNotFound
from ..db.models.follow import Follow
from ..db.models.like import Like
from ..db.models.media import Media
from ..db.models.tweet import Tweet
from ..db.models.user import User


class TweetService:
    @staticmethod
    def create_tweet(
        db: Session, content: str, media_ids: list[int], author_id: int
    ) -> int:
        """Создаёт твит с опциональными медиафайлами."""
        if not author_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "result": False,
                    "error_type": "auth",
                    "error_message": "Unauthorized",
                },
            )

        tweet = Tweet(content=content, author_id=author_id)
        db.add(tweet)
        db.flush()

        if media_ids:
            medias = db.query(Media).filter(Media.id.in_(media_ids)).all()
            for m in medias:
                tweet.medias.append(m)

        db.commit()
        db.refresh(tweet)
        return tweet.id

    @staticmethod
    def delete_tweet(db: Session, tweet_id: int, user_id: int) -> bool:
        """Удаляет твит (только автор)."""
        tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
        if not tweet:
            raise TweetNotFound()
        if tweet.author_id != user_id:
            raise Forbidden()
        db.delete(tweet)
        db.commit()
        return True

    @staticmethod
    def toggle_like(db: Session, tweet_id: int, user_id: int, action: str) -> bool:
        """Добавляет/удаляет лайк (POST=добавить, DELETE=удалить)."""
        tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
        if not tweet:
            raise TweetNotFound()

        if action == "POST":
            existing_like = (
                db.query(Like)
                .filter(Like.tweet_id == tweet_id, Like.user_id == user_id)
                .first()
            )
            if not existing_like:
                like = Like(tweet_id=tweet_id, user_id=user_id)
                db.add(like)
                db.commit()
        else:
            like = (
                db.query(Like)
                .filter(Like.tweet_id == tweet_id, Like.user_id == user_id)
                .first()
            )
            if like:
                db.delete(like)
                db.commit()
        return True

    @staticmethod
    def get_feed(db: Session, user_id: int, limit: int = 20) -> list[Tweet]:
        """
        Возвращает ленту твитов для пользователя user_id (ORM-версия).

        ИНВЕРТИРОВАННАЯ ЛОГИКА (согласована с API /tweets и /follow):
        - Твиты самого user_id + всех его подписчиков
        - Подписчики = пользователи, где Follow.following_id = user_id
                      (т.е. follower_id — это ID тех, кто подписан НА user_id)

        Подзапрос формирует список подписчиков:
        SELECT follower_id FROM follows WHERE following_id = user_id

        Сортировка: по количеству лайков (DESC), затем по created_at (DESC).
        """
        subquery = (
            db.query(Follow.follower_id)
            .filter(Follow.following_id == user_id)
            .subquery()
        )

        tweets = (
            db.query(Tweet)
            .join(User)
            .outerjoin(Like, (Like.tweet_id == Tweet.id))
            # Твиты текущего пользователя и всех, кто на него подписан
            .filter((Tweet.author_id == user_id) | (User.id.in_(subquery)))
            .group_by(Tweet.id, User.id, User.name)
            .order_by(desc(func.count(Like.id)), Tweet.created_at.desc())
            .limit(limit)
            .all()
        )

        return tweets
