from fastapi import APIRouter, HTTPException, status 
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dependencies import SessionDep
from src.posts.schemas import PostCreateSchema, PostResponseSchema, PostUpdateSchema, TagResponseSchema, TagCreateSchema
from src.posts.models import PostModel, TagsModel


posts_router = APIRouter(prefix="/posts", tags=["Posts"])
tags_router = APIRouter(prefix="/tags", tags=["Tags"])


# POSTS ENDPOINTS

@posts_router.post("", response_model=PostResponseSchema)
async def create(data: PostCreateSchema, session: SessionDep):
    tags_query = await session.execute(
        select(TagsModel).where(TagsModel.id.in_(data.tags_ids))
    )
    actual_tags = tags_query.scalars().all()

    new_post = PostModel(
        title = data.title,
        content = data.content,
        tags = actual_tags
    )

    session.add(new_post)
    await session.commit()
    await session.refresh(new_post, attribute_names=["id", "created_at", "updated_at", "tags"])
    return new_post


@posts_router.get("", response_model=list[PostResponseSchema])
async def get_all(session: SessionDep):
    query = await session.execute(select(PostModel).options(selectinload(PostModel.tags)))
    posts = query.scalars().all()
    return posts


@posts_router.get("/{post_id}", response_model=PostResponseSchema)
async def get_by_id(post_id: int, session: SessionDep):
    query = await session.execute(select(PostModel).where(PostModel.id == post_id).options(selectinload(PostModel.tags)))
    post = query.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return post


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@posts_router.patch("/{post_id}", response_model=PostResponseSchema)
async def patch_by_id(post_id: int, data: PostUpdateSchema, session: SessionDep):
    query = await session.execute(select(PostModel).where(PostModel.id == post_id).options(selectinload(PostModel.tags)))
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


# TAGS ENDPOINTS

@tags_router.post("", response_model=TagResponseSchema)
async def create_tag(data: TagCreateSchema, session: SessionDep):
    new_tag = TagsModel(
        title = data.title
    )

    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)
    return new_tag


@tags_router.get("", response_model=list[TagResponseSchema])
async def get_all_tags(session: SessionDep):
    query = await session.execute(select(TagsModel))
    tags = query.scalars().all()
    return tags