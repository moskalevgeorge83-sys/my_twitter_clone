"""Конфигурация приложения и подключение к переменным окружения."""

import os
from typing import Final  # Для неизменяемых констант

from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()


# База данных
DATABASE_URL: Final[str] = os.getenv("DATABASE_URL")  # type: ignore[assignment]
"""
URL подключения к PostgreSQL.

Формат: `postgresql+psycopg2://user:pass@host:port/dbname`

Задаётся через .env:
"""
