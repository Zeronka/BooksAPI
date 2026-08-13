# Books API

REST API для управления библиотекой (авторы и книги) на Python/FastAPI + PostgreSQL.

Проект разработан с разделением ответственности между слоями: Router → Service → Repository → Database. Основная цель — практика построения структурированного backend-приложения с миграциями, тестами и контейнеризацией.

## Возможности

### Authors
- Создание автора
- Получение автора по ID
- Получение списка авторов с пагинацией
- Обновление автора
- Удаление автора

### Books
- Создание книги
- Получение книги по ID
- Получение списка книг с пагинацией
- Обновление книги
- Удаление книги
- Поиск книг по названию
- Получение книг конкретного автора с пагинацией

### Дополнительно
- Валидация входных данных через Pydantic
- Разделение схем для создания, обновления и ответа
- Обработка ошибок 404
- Пагинация с ограничением limit (max 100)
- Unit-тесты (pytest)
- Миграции базы данных (Alembic)
- Docker + Docker Compose

## Стек технологий

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest
- Docker / Docker Compose
- Git / GitHub

## Архитектура

app/
├── database/
│   └── database.py
├── models/
│   ├── author.py
│   └── book.py
├── schemas/
│   ├── author.py
│   └── book.py
├── routers/
│   ├── author.py
│   └── book.py
├── service/
│   ├── author.py
│   └── book.py
├── tests/
│   ├── conftest.py
│   ├── test_authors.py
│   └── test_books.py
└── main.py
plain


## Быстрый старт

### Локально (без Docker)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Zeronka/BooksAPI.git
cd BooksAPI

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать базу данных PostgreSQL (books_db)
# 5. Применить миграции
alembic upgrade head

# 6. Запустить
uvicorn app.main:app --reload

API доступно по адресу: http://localhost:8000/docs
Через Docker
bash

# 1. Клонировать репозиторий
git clone https://github.com/Zeronka/BooksAPI.git
cd BooksAPI

# 2. Запустить
docker-compose up --build

API доступно по адресу: http://localhost:8000/docs
Тесты
bash

pytest -v

Деплой
Приложение развёрнуто на Render: (URL будет добавлен после деплоя)
Связь

    GitHub: Zeronka