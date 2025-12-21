"""Кастомные HTTP исключения с единообразным форматом ответа."""

from fastapi import HTTPException, status


class TweetNotFound(HTTPException):
    """404 ошибка — твит не найден."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "error_type": "not_found",
                "error_message": "Tweet not found",
            },
        )


class UserNotFound(HTTPException):
    """404 ошибка — пользователь не найден."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "result": False,
                "error_type": "not_found",
                "error_message": "User not found",
            },
        )


class Forbidden(HTTPException):
    """403 ошибка — недостаточно прав."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "result": False,
                "error_type": "permission",
                "error_message": "Not enough permissions",
            },
        )
