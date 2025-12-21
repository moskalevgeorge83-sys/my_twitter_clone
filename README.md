# Twitter Clone 

FastAPI + PostgreSQL полноценный Twitter-клон. Лента, follow, лайки, медиа, тесты, Docker.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.2-brightgreen)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-blueviolet)](https://python.org)
[![Tests](https://img.shields.io/badge/Pytest-100%25-brightgreen)](https://pytest.org)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://black.readthedocs.io)
[![CI](https://github.com/moskalevgeorge83-sys/my_twitter_clone/actions/workflows/ci.yml/badge.svg)](https://github.com/moskalevgeorge83-sys/my_twitter_clone/actions)

## ✨ Full Project

http://localhost:8001/ # SPA (Twitter UI)
http://localhost:8001/docs # FastAPI Swagger Docs
http://localhost:8001/redoc # API Docs (ReDoc)


**API Key для теста:** `123` (User1)

## Быстрый запуск (3 команды)

1. Клонировать + .env
git clone https://github.com/moskalevgeorge83-sys/my_twitter_clone.git
cd my_twitter_clone
cp .env.example .env

2. Запустить (backend + postgres)
docker-compose up -d

3. Открыть браузер
http://localhost:8001


## 🛠 Структура проекта

.
├── backend/ # FastAPI API + тесты
│ ├── app/
│ │ ├── api/routes/ # /api/tweets, /api/users, /api/medias
│ │ ├── db/models/ # User, Tweet, Media, Like, Follow
│ │ ├── services/ # Бизнес-логика
│ │ └── schemas/ # Pydantic модели
│ └── tests/ # pytest 100% покрытие
├── frontend/ # Статические файлы SPA
│ ├── static/css/ # Twitter UI CSS/JS
│ └── templates/ # index.html
├── Dockerfile # Python 3.11 + psycopg2
└── docker-compose.yml # postgres:15 + backend:8001


## ✅ Функционал (полностью готово)

| ✓ | Функция | API Endpoint |
|---|---------|--------------|
| ✅ | Лента твитов | `GET /api/tweets/` |
| ✅ | Создать твит | `POST /api/tweets/` |
| ✅ | Удалить твит | `DELETE /api/tweets/{id}` |
| ✅ | Лайк/анлайк | `POST/DELETE /api/tweets/{id}/likes` |
| ✅ | Follow/unfollow | `POST/DELETE /api/users/{id}/follow` |
| ✅ | Профиль | `GET /api/users/{id}, /api/users/me` |
| ✅ | Загрузка медиа | `POST /api/medias/` |
| ✅ | SPA роуты | `/, /profile/1, /static/css/` |

## 🧪 Тестирование (87% покрытие)

Все тесты
docker-compose exec backend pytest

С coverage
docker-compose exec backend pytest --cov=backend/app --cov-report=html

Конкретный тест
docker-compose exec backend pytest tests/test_tweets.py -v


**Тесты:** SPA, API, авторизации, edge cases ✅


## 🔧 Разработка

### Backend (hot reload)
docker-compose up backend # Авто-перезагрузка





### Code Quality
pytest/ && isort backend/ && black backend/


## 📊 API Endpoints

| Метод | Endpoint | Описание | Auth |
|-------|----------|----------|------|
| `GET` | `/api/tweets/` | Лента (популярные от фолловимых) | api-key |
| `POST` | `/api/tweets/` | Создать `{"tweet_data": "...", "tweet_media_ids": []}` | api-key |
| `DELETE` | `/api/tweets/{id}` | Удалить свой твит | api-key |
| `POST` | `/api/tweets/{id}/likes` | Лайк | api-key |
| `DELETE` | `/api/tweets/{id}/likes` | Снять лайк | api-key |
| `GET` | `/api/users/me` | Мой профиль | api-key |
| `GET` | `/api/users/{id}` | Профиль юзера | - |
| `POST` | `/api/users/{id}/follow` | Подписаться | api-key |
| `POST` | `/api/medias/` | Загрузить картинку | api-key |

**Docs:** http://localhost:8001/docs

## 🔑 Тестовые данные

API Key: 123 → User1 (id=1)
API Key: 456 → User2 (id=2)


## 🐳 Docker Compose

services:
postgres: # PostgreSQL 15 (5432)
healthcheck: pg_isready
backend: # FastAPI (8001)
volumes:
- ./backend:/app/backend
- ./frontend:/app/frontend
- ./media:/app/media

**Порты:**

8001 ← Backend SPA + API (единственный порт!)
5432 ← PostgreSQL (локально)

## 📈 Стек технологий

Backend: FastAPI 0.121.2 + SQLAlchemy 
Database: PostgreSQL 15 + psycopg2-binary
Frontend: Статический SPA (CSS/JS/HTML)
DevOps: Docker + docker-compose
Quality: pytest + black + isort 


## 📄 Учебный проект

Используй свободно!
