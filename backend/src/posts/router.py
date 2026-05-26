from fastapi import APIRouter
from sqlalchemy import select
from src.dependencies import SessionDep
from src.posts.schemas import PostCreateSchema, PostResponseSchema
from src.posts.models import PostModel


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=PostResponseSchema)
async def create(data: PostCreateSchema, session: SessionDep):
    new_post = PostModel(
        title = data.title,
        content = data.content
    )

    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


@router.get("", response_model=list[PostResponseSchema])
async def get_all(session: SessionDep):
    query = await session.execute(select(PostModel))
    posts = query.scalars().all()
    return posts