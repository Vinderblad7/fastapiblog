from fastapi import APIRouter, HTTPException, status 
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dependencies import SessionDep, CurrentUserDep
from src.comments.schemas import CommentCreateSchema, CommentResponseSchema, CommentUpdateSchema
from src.comments.models import CommentModel
from src.posts.models import PostModel

comments_router = APIRouter(prefix="/comments", tags=["Comments"])

@comments_router.post("/{post_id}", response_model=CommentResponseSchema)
async def create(post_id: int, data: CommentCreateSchema, session: SessionDep, current_user: CurrentUserDep):
    query = await session.execute(select(PostModel).where(PostModel.id == post_id))
    result = query.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, 
                            detail="Post not found")
    
    new_comment = CommentModel(
        content = data.content,
        user_id= current_user.id,
        post_id = post_id
    )

    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)

    new_comment.user = current_user

    return new_comment

@comments_router.get("/{post_id}", response_model=list[CommentResponseSchema])
async def get_all_by_post(
    post_id: int, 
    session: SessionDep, 
    limit: int = 10,
    offset: int = 0
):
    query = await session.execute(
        select(CommentModel)
        .where(CommentModel.post_id == post_id)
        .options(selectinload(CommentModel.user))
        .limit(limit)
        .offset(offset)
    )
    
    comments = query.scalars().all()
    
    return comments

@comments_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    session: SessionDep,
    current_user: CurrentUserDep
):
    query = await session.execute(
        select(CommentModel)
        .where(CommentModel.id == comment_id)
    )
    comment = query.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this comment"
        )
    
    await session.delete(comment)
    await session.commit()

@comments_router.patch("/{comment_id}", response_model=CommentResponseSchema)
async def update_comment(
    comment_id: int,
    data: CommentUpdateSchema,
    session: SessionDep,
    current_user: CurrentUserDep
):
    query = await session.execute(
        select(CommentModel)
        .where(CommentModel.id == comment_id)
    )
    comment = query.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this comment"
        )
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(comment, key, value)
        
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    comment.user = current_user
    
    return comment