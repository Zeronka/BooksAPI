from fastapi import FastAPI

from app.routers.author import router as author_router
from app.routers.book import router as book_router
from app.routers.user import router as user_router

app = FastAPI()

app.include_router(router=user_router)
app.include_router(router=book_router)
app.include_router(router=author_router)
