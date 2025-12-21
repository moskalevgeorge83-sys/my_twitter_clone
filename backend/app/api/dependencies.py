"""Зависимость аутентификации по API ключу из заголовка."""

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from ..core.security import get_user_by_api_key
from ..db.base import get_db
from ..db.models.user import User

api_key_scheme = APIKeyHeader(name="api-key", auto_error=False)


async def get_user_from_header(
    api_key: str = Depends(api_key_scheme), db: Session = Depends(get_db)
) -> User:
    """
    - api-key из header!
    - api-key валидный → этот пользователь
    - api-key НЕ валидный → 401 ошибка!
    """
    print(f"🔍 api_key='{api_key}'")

    # ✅ Алиасы для демо
    aliases = {"test": "123", "user2": "456", "user3": "789"}
    if api_key in aliases:
        api_key = aliases[api_key]
        print(f"🔄 Alias → '{api_key}'")

    # ✅ Ищем ТОЛЬКО по api-key из header
    if api_key and api_key not in ["null", "undefined", ""]:
        user = get_user_by_api_key(db, api_key)
        if user:
            print(f"✅ Авторизован: {user.name}")
            return user

    # ✅ КИДАЕМ ошибку вместо None!
    raise HTTPException(
        status_code=401,
        detail={
            "result": False,
            "error_type": "auth",
            "error_message": "Invalid api-key",
        },
    )
