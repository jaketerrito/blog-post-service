from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

from src.models import BlogPost

router = APIRouter(prefix="/blog-post")


class UpdateOptions(BaseModel):
    model_config = {"extra": "forbid"}  # This rejects extra fields
    title: str | None = None
    content: str | None = None
    public: bool | None = None


@router.patch("/{blog_post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_blog_post(
    blog_post_id: str, user_id: Annotated[str, Header()], updates: UpdateOptions
) -> None:
    # Find the blog post
    blog_post = await BlogPost.find_one(BlogPost.id == PydanticObjectId(blog_post_id))

    # Check if blog post exists
    if not blog_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found"
        )

    # Verify ownership - ensure author_id matches
    if blog_post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this blog post",
        )

    updates_dict = updates.model_dump(exclude_none=True)
    for key, value in updates_dict.items():
        setattr(blog_post, key, value)

    blog_post.updated_at = datetime.now()
    await blog_post.save()
