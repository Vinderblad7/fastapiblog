from fastapi import APIRouter
from src.posts.router import posts_router, tags_router

main_router = APIRouter(prefix="/api")

main_router.include_router(posts_router)
main_router.include_router(tags_router)