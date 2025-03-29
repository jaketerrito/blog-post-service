from fastapi import status
from pytest_asyncio import fixture

from src.models import BlogPost
from tests.conftest import AUTHOR_ID


@fixture(autouse=True)
async def blog_post():
    blog_post = BlogPost(
        author_id=AUTHOR_ID,
        public=True,
    )
    await blog_post.save()
    yield blog_post
    await blog_post.delete()


def test_all_fields(client, blog_post):
    response = client.patch(
        f"/blog-post/{blog_post.id}",
        headers={"user-id": AUTHOR_ID},
        json={
            "content": "Updated content",
            "title": "Updated title",
            "public": False,
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(
        f"/blog-post/{blog_post.id}",
        headers={"user-id": AUTHOR_ID},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["_id"] == str(blog_post.id)
    assert response.json()["content"] == "Updated content"
    assert response.json()["title"] == "Updated title"
    assert response.json()["public"] is False


def test_invalid_field(client, blog_post):
    response = client.patch(
        f"/blog-post/{blog_post.id}",
        headers={"user-id": AUTHOR_ID},
        json={
            "author_id": "new_author_id",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_not_author(client, blog_post):
    response = client.patch(
        f"/blog-post/{blog_post.id}",
        headers={"user-id": "other"},
        json={
            "content": "new_content",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
