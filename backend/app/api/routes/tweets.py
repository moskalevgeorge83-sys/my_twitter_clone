"""Роуты API для работы с твитами (CRUD + лайки + лента)."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session

from ...api.dependencies import get_user_from_header
from ...db.base import get_db
from ...db.models.user import User
from ...schemas.tweet import TweetCreate
from ...services.tweet_service import TweetService

router = APIRouter(prefix="/tweets", tags=["Tweets"])


@router.post("/", response_model=dict)
async def create_tweet(
    tweet: TweetCreate,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """Создаёт новый твит с опциональными медиафайлами."""
    tweet_id = TweetService.create_tweet(
        db, tweet.tweet_data, tweet.tweet_media_ids, current_user.id
    )
    return {"result": True, "tweet_id": tweet_id}


@router.delete("/{tweet_id}", response_model=dict)
async def delete_tweet(
    tweet_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
) -> dict:
    """Удаляет твит (только автор может удалить)."""
    TweetService.delete_tweet(db, tweet_id, current_user.id)
    return {"result": True}


@router.get("/", response_model=dict)
async def get_feed(
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
):
    """
    Возвращает ленту твитов для current_user.

    ИНВЕРТИРОВАННАЯ ЛОГИКА (согласована с /follow):
    - Показывает твиты самого current_user + всех его подписчиков
    - Подписчики = те пользователи, у кого в follows: follower_id = их_id, following_id = current_user.id
    - Т.е. лента содержит твиты тех, кто "подписан на current_user" (по фронтенд-контракту)

    Сортировка: сначала по количеству лайков (DESC), затем по дате создания (DESC).
    Лимит: 20 твитов.
    """
    if not current_user:
        return {"result": True, "tweets": []}

    # 1. Подписчики (инверсия)
    follower_ids = (
        db.execute(
            text("SELECT follower_id FROM follows WHERE following_id = :user_id"),
            {"user_id": current_user.id},
        )
        .scalars()
        .all()
    )

    author_ids = [current_user.id] + follower_ids

    # 2. Основной запрос с IN и expanding bindparam
    query = text(
        """
        SELECT t.id, t.content, t.created_at, t.author_id, u.name
        FROM tweets t
        JOIN users u ON u.id = t.author_id
        WHERE t.author_id IN :author_ids
        ORDER BY 
            (SELECT COUNT(*) FROM likes l2 WHERE l2.tweet_id = t.id) DESC,
            t.created_at DESC
        LIMIT 20
    """
    ).bindparams(bindparam("author_ids", expanding=True))

    tweets_base = db.execute(query, {"author_ids": author_ids}).fetchall()

    formatted_tweets = []
    for tweet_row in tweets_base:
        tweet_id, content, created_at, author_id, author_name = tweet_row

        attachments = (
            db.execute(
                text(
                    """
                SELECT m.file_path FROM tweet_media tm
                JOIN medias m ON m.id = tm.media_id
                WHERE tm.tweet_id = :tweet_id
            """
                ),
                {"tweet_id": tweet_id},
            )
            .scalars()
            .all()
        )

        likes = db.execute(
            text(
                """
                SELECT l.user_id, u.name 
                FROM likes l
                JOIN users u ON u.id = l.user_id
                WHERE l.tweet_id = :tweet_id
            """
            ),
            {"tweet_id": tweet_id},
        ).fetchall()

        formatted_tweets.append(
            {
                "id": tweet_id,
                "content": content,
                "attachments": list(attachments),
                "author": {"id": author_id, "name": author_name},
                "likes": [{"user_id": x[0], "name": x[1]} for x in likes],
            }
        )

    return {"result": True, "tweets": formatted_tweets}


@router.post("/{tweet_id}/likes", response_model=dict)
@router.delete("/{tweet_id}/likes", response_model=dict)
async def toggle_like(
    tweet_id: int,
    current_user: User = Depends(get_user_from_header),
    db: Session = Depends(get_db),
    request: Request = None,
) -> dict:
    """Переключает лайк/анлайк твита (POST=лайк, DELETE=анлайк)."""
    action = "POST" if request.method == "POST" else "DELETE"
    TweetService.toggle_like(db, tweet_id, current_user.id, action)
    return {"result": True}
