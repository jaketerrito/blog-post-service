from datetime import datetime, timedelta

import pytest
from beanie import PydanticObjectId
from fastapi import status
from pytest_asyncio import fixture

from src.models import BlogPost
from tests.conftest import AUTHOR_ID


@fixture()
async def blog_post():
    """Create a test blog post"""
    blog_post = BlogPost(
        author_id=AUTHOR_ID,
        public=True,
    )
    await blog_post.save()
    yield blog_post
    await blog_post.delete()


@pytest.mark.parametrize("user_id", [AUTHOR_ID, None, "other"])
def test_exists_public(client, blog_post, user_id):
    headers = {"user-id": user_id} if user_id is not None else {}
    response = client.get(
        f"/blog-post/{blog_post.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["_id"] == str(blog_post.id)


@fixture()
async def private_blog_post():
    """Create a test blog post"""
    blog_post = BlogPost(
        author_id=AUTHOR_ID,
    )
    await blog_post.save()
    yield blog_post
    await blog_post.delete()


def test_exists_not_public(client, private_blog_post):
    # Test author access to private post
    response = client.get(
        f"/blog-post/{private_blog_post.id}",
        headers={"user-id": AUTHOR_ID},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["_id"] == str(private_blog_post.id)

    response = client.get(
        f"/blog-post/{private_blog_post.id}",
        headers={"user-id": "other"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_not_exist(client):
    non_existent_id = PydanticObjectId()

    response = client.get(
        f"/blog-post/{non_existent_id}",
        headers={"user-id": "other"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


PUBLIC_POST_COUNT = 10


@fixture()
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
        "/blog-post",
        params={"author_id": AUTHOR_ID},
    )
    assert response.status_code == status.HTTP_200_OK
    blog_posts = response.json()
    assert len(blog_posts) == PUBLIC_POST_COUNT
    assert blog_posts[0]["title"] == "9"  # sorted so newest is first
    assert blog_posts[-1]["title"] == "0"


def test_get_blog_posts_by_author_pagination(client, blog_posts):
    response = client.get(
        "/blog-post",
        params={"author_id": AUTHOR_ID, "skip": PUBLIC_POST_COUNT - 1, "limit": 2},
    )
    assert response.status_code == status.HTTP_200_OK
    blog_posts = response.json()
    assert len(blog_posts) == 1
    assert blog_posts[0]["title"] == "0"


def test_get_blog_posts_by_author_private(client, blog_posts):
    response = client.get(
        "/blog-post",
        params={"author_id": AUTHOR_ID},
        headers={"user-id": AUTHOR_ID},
    )
    assert response.status_code == status.HTTP_200_OK
    blog_posts = response.json()
    assert len(blog_posts) == PUBLIC_POST_COUNT + 1
    assert blog_posts[-1]["title"] == "private"


def test_get_blog_posts_by_nonexistent_author(client, blog_posts):
    response = client.get(
        "/blog-post",
        params={"author_id": "NOTREAL"},
    )
    assert response.status_code == status.HTTP_200_OK
    blog_posts = response.json()
    assert len(blog_posts) == 0
