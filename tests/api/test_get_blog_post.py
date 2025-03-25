import pytest
from beanie import PydanticObjectId
from pytest_asyncio import fixture as async_fixture

from src.models import BlogPost
from tests.conftest import AUTHOR_ID


@async_fixture()
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
    response = client.get(
        "/blog-post",
        params={"blog_post_id": blog_post.id, "user_id": user_id},
    )
    assert response.status_code == 200
    assert response.json()["_id"] == str(blog_post.id)


@async_fixture()
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
        "/blog-post",
        params={"blog_post_id": private_blog_post.id, "user_id": AUTHOR_ID},
    )
    assert response.status_code == 200
    assert response.json()["_id"] == str(private_blog_post.id)

    response = client.get(
        "/blog-post",
        params={"blog_post_id": private_blog_post.id, "user_id": "other"},
    )
    assert response.status_code == 403


def test_not_exist(client):
    non_existent_id = PydanticObjectId()

    response = client.get(
        "/blog-post",
        params={"blog_post_id": non_existent_id, "user_id": "other"},
    )
    assert response.status_code == 404
