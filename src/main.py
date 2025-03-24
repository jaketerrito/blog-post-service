import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import pymongo
from beanie import PydanticObjectId
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from src.database import init_database
from src.models import BlogPost

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient("mongodb://root:example@mongodb:27017")
    await init_database(client)
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)


@app.get("/blog-post")
async def get_blog_post(user_id: str, blog_post_id: str) -> BlogPost:
    print(blog_post_id)
    print(await BlogPost.all().to_list())
    # First, find the blog post by ID
    blog_post = await BlogPost.find_one(BlogPost.id == PydanticObjectId(blog_post_id))
    print(blog_post)
    # Check if blog post exists
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Check if user is authorized to view the post
    if not (blog_post.public or blog_post.author_id == user_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this blog post"
        )

    return blog_post


@app.put("/blog-post")
async def create_blog_post(user_id: str, title: str) -> PydanticObjectId:
    blog_post = BlogPost(
        author_id=user_id,
        public=False,
        title=title,
    )
    await blog_post.save()
    return str(blog_post.id)


class UpdateOptions(BaseModel):
    model_config = {"extra": "forbid"}  # This rejects extra fields
    title: str | None = None
    content: str | None = None
    public: bool | None = None


class UpdateBlogPost(BaseModel):
    blog_post_id: str
    user_id: str
    updates: UpdateOptions


@app.patch("/blog-post")
async def update_blog_post(params: UpdateBlogPost) -> BlogPost:
    # Find the blog post
    blog_post = await BlogPost.find_one(
        BlogPost.id == PydanticObjectId(params.blog_post_id)
    )

    # Check if blog post exists
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Verify ownership - ensure author_id matches
    if blog_post.author_id != params.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this blog post"
        )

    updates_dict = params.updates.model_dump(exclude_none=True)
    for key, value in updates_dict.items():
        setattr(blog_post, key, value)

    blog_post.updated_at = datetime.now()  # Update the timestamp
    await blog_post.save()

    return blog_post


@app.get("/blog-posts-by-author")
async def get_blog_posts_by_author(
    author_id: str, skip: int = 0, limit: int = 20
) -> List[BlogPost]:
    # Execute query with sorting and pagination
    return (
        await BlogPost.find({"author_id": author_id, "public": True})
        .sort([("created_at", pymongo.DESCENDING)])
        .skip(skip)
        .limit(limit)
        .to_list()
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
