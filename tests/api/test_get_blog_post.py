from datetime import datetime

import pytest
from beanie import PydanticObjectId
from fastapi import HTTPException
from pytest_asyncio import fixture as async_fixture

from src.main import get_blog_post
from src.models import BlogPost

BLOG_POST_ID = PydanticObjectId()
AUTHOR_ID = "test_author_id"
USER_ID = "test_user_id"


@async_fixture(autouse=True)
async def blog_post():
    """Create a test blog post"""
    blog_post = BlogPost(
        id=BLOG_POST_ID,
        author_id=AUTHOR_ID,
        public=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        content="Test content",
    )
    await blog_post.save()
    yield blog_post
    await blog_post.delete()


@pytest.mark.asyncio
async def test_exists_public():
    # Test author access
    response = await get_blog_post(user_id=AUTHOR_ID, blog_post_id=BLOG_POST_ID)
    assert response.id == BLOG_POST_ID

    # Test other user access to public post
    response = await get_blog_post(user_id=USER_ID, blog_post_id=BLOG_POST_ID)
    assert response.id == BLOG_POST_ID


@pytest.mark.asyncio
async def test_exists_not_public(blog_post):
    # Make the blog post private
    blog_post.public = False
    await blog_post.save()

    # Test author access to private post
    response = await get_blog_post(user_id=AUTHOR_ID, blog_post_id=BLOG_POST_ID)
    assert response.id == BLOG_POST_ID

    # Test other user access to private post - should get 403
    with pytest.raises(HTTPException) as excinfo:
        await get_blog_post(user_id=USER_ID, blog_post_id=BLOG_POST_ID)

    assert excinfo.value.status_code == 403
    assert "Not authorized" in excinfo.value.detail


@pytest.mark.asyncio
async def test_not_exist():
    non_existent_id = PydanticObjectId()

    with pytest.raises(HTTPException) as excinfo:
        await get_blog_post(user_id=USER_ID, blog_post_id=non_existent_id)

    assert excinfo.value.status_code == 404
    assert "not found" in excinfo.value.detail
