FROM python:3.11-slim

WORKDIR /app

# Сначала зависимости — чтобы Docker кэшировал слой
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Утилита для проверки готовности Postgres
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Копируем весь код
COPY . .

# Entrypoint ждёт Postgres и гоняет миграции
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Запуск приложения (передаётся в entrypoint через exec "$@")
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]