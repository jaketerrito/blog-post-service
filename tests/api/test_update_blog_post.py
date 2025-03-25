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
    response = client.get(
        "/blog-post",
        params={"blog_post_id": str(blog_post.id), "user_id": AUTHOR_ID},
    )
    assert response.status_code == 200
    original_blog_post = response.json()

    response = client.patch(
        "/blog-post",
        json={
            "blog_post_id": str(blog_post.id),
            "user_id": AUTHOR_ID,
            "updates": {
                "content": "Updated content",
                "title": "Updated title",
                "public": False,
            },
        },
    )
    assert response.status_code == 200
    assert response.json()["_id"] == str(blog_post.id)
    assert response.json()["content"] == "Updated content"
    assert response.json()["title"] == "Updated title"
    assert response.json()["public"] is False
    assert response.json() != original_blog_post
    patched_blog_post = response.json()

    response = client.get(
        "/blog-post",
        params={"blog_post_id": str(blog_post.id), "user_id": AUTHOR_ID},
    )
    assert response.status_code == 200
    assert response.json() == patched_blog_post


def test_invalid_field(client, blog_post):
    response = client.patch(
        "/blog-post",
        json={
            "blog_post_id": str(blog_post.id),
            "user_id": AUTHOR_ID,
            "updates": {
                "author_id": "new_author_id",
            },
        },
    )
    assert response.status_code == 422


def test_not_author(client, blog_post):
    response = client.patch(
        "/blog-post",
        json={
            "blog_post_id": str(blog_post.id),
            "user_id": "other",
            "updates": {
                "content": "new_content",
            },
        },
    )
    assert response.status_code == 403
