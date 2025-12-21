"""Безопасность: поиск пользователей по API ключу."""

from sqlalchemy.orm import Session

from ..db.models.user import User


def get_user_by_api_key(db: Session, api_key: str) -> User | None:
    """Находит пользователя по API ключу.

    Args:
        db: SQLAlchemy сессия
        api_key: Уникальный API ключ пользователя

    Returns:
        User | None: Пользователь или None если не найден
    """
    return db.query(User).filter(User.api_key == api_key).first()


def create_test_users(db: Session) -> None:
    """Создаёт тестовых пользователей при первом запуске.

    API ключи для тестов:
    * User1 → "123"
    * User2 → "456"
    * User3 → "789"

    Args:
        db: SQLAlchemy сессия
    """
    if db.query(User).first():
        return

    test_users = [
        {"name": "User1", "api_key": "123"},
        {"name": "User2", "api_key": "456"},
        {"name": "User3", "api_key": "789"},
    ]

    for user_data in test_users:
        user = User(**user_data)
        db.add(user)
    db.commit()
