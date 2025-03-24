from datetime import datetime

import pytest
from beanie import PydanticObjectId
from fastapi import HTTPException
from pydantic_core import ValidationError
from pytest_asyncio import fixture

from src.main import UpdateBlogPost, update_blog_post
from src.models import BlogPost

AUTHOR_ID = "test_author_id"
BLOG_POST_ID = PydanticObjectId()


@fixture(autouse=True)
async def blog_post():
    """Create a test blog post"""
    blog_post = BlogPost(
        id=BLOG_POST_ID,
        author_id=AUTHOR_ID,
        title="Test title",
        public=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        content="Test content",
    )
    await blog_post.save()
    yield blog_post
    await blog_post.delete()


@pytest.mark.asyncio
async def test_all_fields():
    # Test author access
    updated_blog_post = await update_blog_post(
        params=UpdateBlogPost(
            user_id=AUTHOR_ID,
            blog_post_id=str(BLOG_POST_ID),
            updates={
                "content": "Updated content",
                "title": "Updated title",
                "public": False,
            },
        ),
    )
    assert updated_blog_post.id == BLOG_POST_ID
    assert updated_blog_post.content == "Updated content"
    assert updated_blog_post.title == "Updated title"
    assert updated_blog_post.public is False


@pytest.mark.asyncio
async def test_invalid_field():
    # Test author access
    with pytest.raises(ValidationError):
        await update_blog_post(
            params=UpdateBlogPost(
                user_id=AUTHOR_ID,
                blog_post_id=str(BLOG_POST_ID),
                updates={
                    "author_id": "new_author_id",
                },
            ),
        )


@pytest.mark.asyncio
async def test_not_author():
    # Test author access
    with pytest.raises(HTTPException) as excinfo:
        await update_blog_post(
            params=UpdateBlogPost(
                user_id="NOT_AUTHOR_ID",
                blog_post_id=str(BLOG_POST_ID),
                updates={"content": "Updated content"},
            ),
        )
    assert excinfo.value.status_code == 403
    assert "Not authorized" in excinfo.value.detail

    blog_post = await BlogPost.find_one(BlogPost.id == BLOG_POST_ID)
    assert blog_post.content == "Test content"
