from typing import Annotated, List

import pymongo
from beanie import PydanticObjectId
from fastapi import APIRouter, Header, HTTPException, status

from src.models import BlogPost

router = APIRouter(prefix="/blog-post")


@router.get("/{blog_post_id}", status_code=status.HTTP_200_OK)
async def get_blog_post(
    blog_post_id: str, user_id: Annotated[str | None, Header()] = None
) -> BlogPost:
    blog_post = await BlogPost.find_one(BlogPost.id == PydanticObjectId(blog_post_id))

    if not blog_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found"
        )

    # Check if user is authorized to view the post
    if not (blog_post.public or blog_post.author_id == user_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this blog post"
        )

    return blog_post


@router.get("", status_code=status.HTTP_200_OK)
async def get_blog_posts_by_author(
    author_id: str,
    skip: int = 0,
    limit: int = 20,
    user_id: Annotated[str | None, Header()] = None,
) -> List[BlogPost]:
    query = {"author_id": author_id}
    if user_id != author_id:
        query["public"] = True
    return (
        await BlogPost.find(query)
        .sort([("created_at", pymongo.DESCENDING)])
        .skip(skip)
        .limit(limit)
        .to_list()
    )
