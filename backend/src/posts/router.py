from fastapi import APIRouter, HTTPException, status 
from sqlalchemy import select
from src.dependencies import SessionDep
from src.posts.schemas import PostCreateSchema, PostResponseSchema, PostUpdateSchema
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


@router.get("/{post_id}", response_model=PostResponseSchema)
async def get_by_id(post_id: int, session: SessionDep):
    query = await session.execute(select(PostModel).where(PostModel.id == post_id))
    post = query.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(post_id: int, session: SessionDep):
    query = await session.execute(select(PostModel).where(PostModel.id == post_id))
    post = query.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    await session.delete(post)
    await session.commit()


@router.patch("/{post_id}", response_model=PostResponseSchema)
async def patch_by_id(post_id: int, data: PostUpdateSchema, session: SessionDep):
    query = await session.execute(select(PostModel).where(PostModel.id == post_id))
    post = query.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(post, key, value)
        
    session.add(post)
    await session.commit()
    await session.refresh(post)
    
    return post