import pytest
from beanie import PydanticObjectId

from src.main import create_blog_post
from src.models import BlogPost

AUTHOR_ID = "test_author_id"
TITLE = "Test title"


@pytest.mark.asyncio
async def test_create_blog_post():
    blog_post_id = await create_blog_post(user_id=AUTHOR_ID, title=TITLE)
    blog_post = await BlogPost.find_one(BlogPost.id == PydanticObjectId(blog_post_id))
    assert blog_post is not None
    assert blog_post.title == TITLE
    assert blog_post.author_id == AUTHOR_ID
    assert blog_post.public is False
