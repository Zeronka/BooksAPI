# Books API

REST API для управления библиотекой (авторы и книги) на Python/FastAPI + PostgreSQL.

Проект разработан с разделением ответственности между слоями:

**Router → Service → Repository → Database**

Основная цель проекта — практика построения структурированного backend-приложения с миграциями, тестами и контейнеризацией.

## Возможности

### Authors

* Создание автора
* Получение автора по ID
* Получение списка авторов с пагинацией
* Обновление автора
* Удаление автора

### Books

* Создание книги
* Получение книги по ID
* Получение списка книг с пагинацией
* Обновление книги
* Удаление книги
* Поиск книг по названию
* Получение книг конкретного автора с пагинацией

### Дополнительно

* Валидация входных данных через Pydantic
* Разделение схем для создания, обновления и ответа
* Обработка ошибок 404
* Пагинация с ограничением `limit` (max 100)
* Unit-тесты (pytest)
* Миграции базы данных (Alembic)
* Docker + Docker Compose

## Стек технологий

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* Pytest
* Docker / Docker Compose
* Git / GitHub

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


## Быстрый старт

### Локально (без Docker)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Zeronka/BooksAPI.git
cd BooksAPI

# 2. Создать виртуальное окружение
python -m venv venv

# 3. Активировать виртуальное окружение
source venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Создать базу данных PostgreSQL
# Название базы: books_db

# 6. Применить миграции
alembic upgrade head

# 7. Запустить приложение
uvicorn app.main:app --reload
```

API и Swagger UI доступны по адресу:

http://localhost:8000/docs

### Через Docker

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Zeronka/BooksAPI.git
cd BooksAPI

# 2. Запустить контейнеры
docker-compose up --build
```

API и Swagger UI доступны по адресу:

http://localhost:8000/docs

## Тесты

Для запуска тестов:

```bash
pytest -v
```

Тестами покрыты основные операции с авторами и книгами, включая:

* создание;
* получение;
* обновление;
* удаление;
* поиск книг;
* пагинацию;
* валидацию параметров пагинации;
* обработку ошибок 404.

## Деплой

Приложение развёрнуто на Render: https://booksapi-1-hkii.onrender.com/docs

## Связь

GitHub: [Zeronka](https://github.com/Zeronka)
