from datetime import datetime, timedelta

import pytest_asyncio

from src.models import BlogPost
from tests.conftest import AUTHOR_ID

PUBLIC_POST_COUNT = 10


@pytest_asyncio.fixture
async def blog_posts():
    for i in range(PUBLIC_POST_COUNT):
        blog_post = BlogPost(
            author_id=AUTHOR_ID,
            title=str(i),
            public=True,
            created_at=datetime.now() + timedelta(days=i),
        )
        await blog_post.save()

    blog_post = BlogPost(
        author_id=AUTHOR_ID,
        title="private",
        public=False,
        created_at=datetime.now() - timedelta(days=1),
    )
    await blog_post.save()


def test_get_blog_posts_by_author(client, blog_posts):
    response = client.get(
        "/blog-posts-by-author",
        params={"author_id": AUTHOR_ID},
    )
    assert response.status_code == 200
    blog_posts = response.json()
    assert len(blog_posts) == PUBLIC_POST_COUNT
    assert blog_posts[0]["title"] == "9"  # sorted so newest is first
    assert blog_posts[-1]["title"] == "0"


def test_get_blog_posts_by_author_pagination(client, blog_posts):
    response = client.get(
        "/blog-posts-by-author",
        params={"author_id": AUTHOR_ID, "skip": PUBLIC_POST_COUNT - 1, "limit": 2},
    )
    assert response.status_code == 200
    blog_posts = response.json()
    assert len(blog_posts) == 1
    assert blog_posts[0]["title"] == "0"


def test_get_blog_posts_by_author_private(client, blog_posts):
    response = client.get(
        "/blog-posts-by-author",
        params={"author_id": AUTHOR_ID, "user_id": AUTHOR_ID},
    )
    assert response.status_code == 200
    blog_posts = response.json()
    assert len(blog_posts) == PUBLIC_POST_COUNT + 1
    assert blog_posts[-1]["title"] == "private"


def test_get_blog_posts_by_nonexistent_author(client, blog_posts):
    response = client.get(
        "/blog-posts-by-author",
        params={"author_id": "NOTREAL"},
    )
    assert response.status_code == 200
    blog_posts = response.json()
    assert len(blog_posts) == 0
