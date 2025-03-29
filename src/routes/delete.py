from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Header, HTTPException, status

from src.models import BlogPost

router = APIRouter(prefix="/blog-post")


@router.delete("/{blog_post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(blog_post_id: str, user_id: Annotated[str, Header()]):
    blog_post = await BlogPost.find_one(BlogPost.id == PydanticObjectId(blog_post_id))

    if not blog_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found"
        )
    if blog_post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this blog post",
        )

    await blog_post.delete()
