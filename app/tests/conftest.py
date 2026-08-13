import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db

# SQLite в памяти для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаём таблицы один раз перед всеми тестами
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Подменяем зависимость
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Очищаем таблицы перед каждым тестом
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as c:
        yield c