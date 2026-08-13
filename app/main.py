from app.routers.book import router as book_router
from app.routers.author import router as author_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=book_router)
app.include_router(router=author_router)