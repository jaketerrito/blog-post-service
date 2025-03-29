from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Header, status

from src.models import BlogPost

router = APIRouter(prefix="/blog-post")


@router.put("", status_code=status.HTTP_201_CREATED)
async def create_blog_post(user_id: Annotated[str, Header()]) -> PydanticObjectId:
    blog_post = BlogPost(
        author_id=user_id,
        public=False,
    )
    await blog_post.save()
    return str(blog_post.id)
