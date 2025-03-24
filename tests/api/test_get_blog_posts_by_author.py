from datetime import datetime, timedelta

import pytest
from beanie import PydanticObjectId

from src.main import get_blog_posts_by_author
from src.models import BlogPost

AUTHOR_ID = "test_author_id"


@pytest.mark.asyncio
async def test_exists_public():
    count = 10
    for i in range(count):
        blog_post = BlogPost(
            id=PydanticObjectId(),
            author_id=AUTHOR_ID,
            title=str(i),
            public=True,
            created_at=datetime.now() + timedelta(days=i),
            updated_at=datetime.now(),
            content="Test content",
        )
        await blog_post.save()

    blog_post = BlogPost(
        id=PydanticObjectId(),
        author_id=AUTHOR_ID,
        title="private",
        public=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        content="Test content",
    )
    await blog_post.save()

    # Test author access
    blog_posts = await get_blog_posts_by_author(author_id=AUTHOR_ID)
    assert len(blog_posts) == count
    assert blog_posts[0].title == "9"  # sorted so newest is first

    blog_posts = await get_blog_posts_by_author(author_id=AUTHOR_ID, skip=1, limit=1)
    assert len(blog_posts) == 1
    assert blog_posts[0].title == "8"

    blog_posts = await get_blog_posts_by_author(author_id=AUTHOR_ID, skip=9, limit=1000)
    assert len(blog_posts) == 1
    assert blog_posts[0].title == "0"

    blog_posts = await get_blog_posts_by_author(author_id=AUTHOR_ID, skip=1000, limit=1)
    assert len(blog_posts) == 0
