import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import pymongo
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


@app.get("/get_blog_post")
async def get_blog_post(user_id: str, blog_post_id: str) -> BlogPost:
    print("getting this one")
    print(blog_post_id)
    # First, find the blog post by ID
    blog_post = await BlogPost.find_one(BlogPost.id == blog_post_id)
    print("why")
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


@app.get("/create_blog_post")
async def create_blog_post(user_id: str) -> str:
    blog_post = BlogPost(
        author_id=user_id,
        public=False,
    )
    await blog_post.save()
    print("created")
    print(blog_post)
    return blog_post.id.__str__()


class UpdateBlogPostContent(BaseModel):
    blog_post_id: str
    user_id: str
    content: str


@app.patch("/update_blog_post/content")
async def update_blog_post_content(params: UpdateBlogPostContent):
    # Find the blog post
    blog_post = await BlogPost.find_one(BlogPost.id == params.blog_post_id)

    # Check if blog post exists
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Verify ownership - ensure author_id matches
    if blog_post.author_id != params.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this blog post"
        )

    # Update and save the blog post
    blog_post.content = params.content
    blog_post.updated_at = datetime.utcnow()  # Update the timestamp
    await blog_post.save()

    return {"status": "success", "message": "Blog post updated successfully"}


class UpdateBlogPostPublic(BaseModel):
    id: str
    user_id: str
    public: bool


@app.patch("/update_blog_post/public")
async def update_blog_post_public(params: UpdateBlogPostPublic):
    # Find the blog post
    blog_post = await BlogPost.find_one(BlogPost.id == params.id)

    # Check if blog post exists
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Verify ownership - ensure author_id matches
    if blog_post.author_id != params.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this blog post"
        )

    # Update and save the blog post
    blog_post.public = params.public
    await blog_post.save()

    return "Success"


@app.get("/get_public_blog_posts")
async def get_public_blog_posts(
    author_id: str, skip: int = 0, limit: int = 20
) -> List[BlogPost]:
    # Execute query with sorting and pagination
    return (
        await BlogPost.find(BlogPost.public & BlogPost.author_id == author_id)
        .sort([("created_at", pymongo.DESCENDING)])
        .skip(skip)
        .limit(limit)
        .to_list()
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
